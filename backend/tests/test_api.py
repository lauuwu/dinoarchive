"""
Tests automáticos de DinoArchive.

Usan una base de datos SQLite en memoria para no depender de Postgres.
Cada test arranca con la base limpia — no hay datos compartidos entre tests.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Apuntamos a SQLite en memoria antes de importar la app
os.environ["DATABASE_URL"] = "sqlite:///./test_tmp.db"
os.environ["UPLOAD_DIR"] = "/tmp/dinoarchive_test_uploads"

from app.main import app
from app.database import Base, get_db

# Motor de prueba separado del de producción
TEST_DB_URL = "sqlite:///./test_tmp.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    """Crea las tablas antes de cada test y las borra al terminar."""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


client = TestClient(app)


# ── Test 1: la API está viva ──────────────────────────────────────────────────
def test_root():
    """GET / debe devolver 200 y el mensaje de bienvenida."""
    response = client.get("/")
    assert response.status_code == 200
    assert "DinoArchive" in response.json()["message"]


# ── Test 2: registro de usuario ───────────────────────────────────────────────
def test_register_user():
    """POST /auth/register debe crear un usuario y devolver 201."""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@dinoarchive.com",
        "password": "testpass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@dinoarchive.com"
    assert data["score"] == 0
    assert "hashed_password" not in data  # nunca debe exponerse


# ── Test 3: registro duplicado es rechazado ───────────────────────────────────
def test_register_duplicate_email():
    """Registrar el mismo email dos veces debe devolver 400."""
    payload = {
        "username": "user1",
        "email": "dup@dinoarchive.com",
        "password": "pass"
    }
    client.post("/auth/register", json=payload)

    payload["username"] = "user2"
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


# ── Test 4: login exitoso devuelve token ─────────────────────────────────────
def test_login_returns_token():
    """POST /auth/login con credenciales válidas debe devolver un access_token."""
    client.post("/auth/register", json={
        "username": "loginuser",
        "email": "login@dinoarchive.com",
        "password": "mypassword"
    })
    response = client.post("/auth/login", data={
        "username": "loginuser",
        "password": "mypassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# ── Test 5: lista de dinosaurios ──────────────────────────────────────────────
def test_get_dinos_empty():
    """GET /dinos/ debe devolver 200 con lista vacía si no hay datos."""
    response = client.get("/dinos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── Test 6: blog público accesible sin login ──────────────────────────────────
def test_blog_list_public():
    """GET /blog/ debe devolver 200 sin necesidad de autenticación."""
    response = client.get("/blog/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── Test 7: crear post de blog sin ser admin es rechazado ────────────────────
def test_blog_create_requires_admin():
    """POST /blog/ sin token debe devolver 401."""
    response = client.post("/blog/", json={
        "title": "Test post",
        "content": "Contenido de prueba"
    })
    assert response.status_code == 401

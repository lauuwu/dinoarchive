from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, dinos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DinoArchive API",
    description="Base de datos enciclopédica de dinosaurios",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dinos.router)

@app.get("/")
def root():
    return {"message": "🦕 DinoArchive API funcionando"}

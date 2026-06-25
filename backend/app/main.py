from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routers import auth, dinos, quiz, blog, gallery, admin
from .routers.gallery import UPLOAD_DIR

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DinoArchive API",
    description="Base de datos enciclopédica de dinosaurios",
    version="0.2.0"
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
app.include_router(quiz.router)
app.include_router(blog.router)
app.include_router(gallery.router)
app.include_router(admin.router)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/")
def root():
    return {"message": "🦕 DinoArchive API funcionando"}

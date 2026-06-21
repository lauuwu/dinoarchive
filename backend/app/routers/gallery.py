import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import GalleryImage, User
from ..schemas import GalleryImageOut
from ..auth_utils import get_current_admin

router = APIRouter(prefix="/gallery", tags=["gallery"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def _to_out(img: GalleryImage) -> GalleryImageOut:
    return GalleryImageOut(
        id=img.id,
        title=img.title,
        caption=img.caption,
        filename=img.filename,
        created_at=img.created_at,
        uploader_username=img.uploader.username,
    )


@router.get("/", response_model=List[GalleryImageOut])
def list_images(db: Session = Depends(get_db)):
    images = db.query(GalleryImage).order_by(GalleryImage.created_at.desc()).all()
    return [_to_out(i) for i in images]


@router.post("/", response_model=GalleryImageOut, status_code=201)
async def upload_image(
    title: str = Form(...),
    caption: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Formato no permitido. Usá JPEG, PNG, WEBP o GIF.",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="La imagen supera el tamaño máximo de 5MB.")

    extension = os.path.splitext(file.filename)[1].lower() or ".jpg"
    unique_name = f"{uuid.uuid4().hex}{extension}"
    filepath = os.path.join(UPLOAD_DIR, unique_name)

    with open(filepath, "wb") as f:
        f.write(contents)

    new_image = GalleryImage(
        title=title,
        caption=caption,
        filename=unique_name,
        uploader_id=current_admin.id,
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return _to_out(new_image)


@router.delete("/{image_id}", status_code=204)
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    image = db.query(GalleryImage).filter(GalleryImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    filepath = os.path.join(UPLOAD_DIR, image.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.delete(image)
    db.commit()

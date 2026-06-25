from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User
from ..schemas import UserOut
from ..auth_utils import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Lista todos los usuarios. Solo admins."""
    return db.query(User).order_by(User.score.desc()).all()


@router.patch("/users/{user_id}/promote", response_model=UserOut)
def promote_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Da permisos de admin a un usuario."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.is_admin = True
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}/demote", response_model=UserOut)
def demote_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Quita permisos de admin a un usuario (no puede quitarse a sí mismo)."""
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="No podés quitarte los permisos a vos mismo")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.is_admin = False
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Elimina un usuario (no puede eliminarse a sí mismo)."""
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="No podés eliminar tu propia cuenta desde acá")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()

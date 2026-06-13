from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Dinosaur
from ..schemas import DinosaurCreate, DinosaurOut

router = APIRouter(prefix="/dinos", tags=["dinosaurs"])

@router.get("/", response_model=List[DinosaurOut])
def list_dinos(db: Session = Depends(get_db)):
    return db.query(Dinosaur).all()

@router.get("/{dino_id}", response_model=DinosaurOut)
def get_dino(dino_id: int, db: Session = Depends(get_db)):
    dino = db.query(Dinosaur).filter(Dinosaur.id == dino_id).first()
    if not dino:
        raise HTTPException(status_code=404, detail="Dinosaurio no encontrado")
    return dino

@router.post("/", response_model=DinosaurOut, status_code=201)
def create_dino(dino: DinosaurCreate, db: Session = Depends(get_db)):
    new_dino = Dinosaur(**dino.model_dump())
    db.add(new_dino)
    db.commit()
    db.refresh(new_dino)
    return new_dino

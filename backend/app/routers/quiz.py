from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random
from ..database import get_db
from ..models import QuizQuestion, Dinosaur, User
from ..schemas import QuizQuestionCreate, QuizQuestionOut, AnswerSubmit, AnswerResult
from ..auth_utils import get_current_user

router = APIRouter(prefix="/quiz", tags=["quiz"])

@router.post("/", response_model=QuizQuestionOut, status_code=201)
def create_question(q: QuizQuestionCreate, db: Session = Depends(get_db)):
    dino = db.query(Dinosaur).filter(Dinosaur.id == q.dinosaur_id).first()
    if not dino:
        raise HTTPException(status_code=404, detail="Dinosaurio no encontrado")
    new_q = QuizQuestion(**q.model_dump())
    db.add(new_q)
    db.commit()
    db.refresh(new_q)
    return new_q

@router.get("/dino/{dino_id}", response_model=List[QuizQuestionOut])
def get_questions_for_dino(dino_id: int, db: Session = Depends(get_db)):
    return db.query(QuizQuestion).filter(QuizQuestion.dinosaur_id == dino_id).all()

@router.post("/answer", response_model=AnswerResult)
def submit_answer(
    answer: AnswerSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(QuizQuestion).filter(QuizQuestion.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    is_correct = answer.chosen_answer.strip().lower() == question.correct_answer.strip().lower()
    points = question.points if is_correct else 0

    if is_correct:
        current_user.score += points
        db.commit()

    return AnswerResult(
        correct=is_correct,
        points_awarded=points,
        new_score=current_user.score,
        correct_answer=question.correct_answer
    )

@router.get("/leaderboard", response_model=List[dict])
def leaderboard(db: Session = Depends(get_db)):
    top_users = db.query(User).order_by(User.score.desc()).limit(10).all()
    return [{"username": u.username, "score": u.score} for u in top_users]

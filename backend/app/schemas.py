from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    score: int
    created_at: datetime
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class DinosaurCreate(BaseModel):
    name: str
    period: Optional[str] = None
    diet: Optional[str] = None
    length_m: Optional[str] = None
    description: Optional[str] = None
    fun_fact: Optional[str] = None
    image_url: Optional[str] = None

class DinosaurOut(DinosaurCreate):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

class QuizQuestionCreate(BaseModel):
    dinosaur_id: int
    question: str
    correct_answer: str
    wrong_answer_1: str
    wrong_answer_2: str
    points: Optional[int] = 10
    fact: Optional[str] = None
    difficulty: Optional[str] = "easy"

class QuizQuestionOut(BaseModel):
    id: int
    dinosaur_id: int
    question: str
    correct_answer: str
    wrong_answer_1: str
    wrong_answer_2: str
    points: int
    fact: Optional[str] = None
    difficulty: str
    model_config = {"from_attributes": True}

class AnswerSubmit(BaseModel):
    question_id: int
    chosen_answer: str

class AnswerResult(BaseModel):
    correct: bool
    points_awarded: int
    new_score: int
    correct_answer: str

class BlogPostCreate(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content: str
    image_url: Optional[str] = None

class BlogPostOut(BaseModel):
    id: int
    title: str
    excerpt: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    created_at: datetime
    author_username: str
    model_config = {"from_attributes": True}

class GalleryImageOut(BaseModel):
    id: int
    title: str
    caption: Optional[str] = None
    filename: str
    created_at: datetime
    uploader_username: str
    model_config = {"from_attributes": True}

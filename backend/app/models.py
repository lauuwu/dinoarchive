from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    blog_posts = relationship("BlogPost", back_populates="author")

class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    excerpt = Column(String(280))
    content = Column(Text, nullable=False)
    image_url = Column(String(255))
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author = relationship("User", back_populates="blog_posts")

class GalleryImage(Base):
    __tablename__ = "gallery_images"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    caption = Column(String(280))
    filename = Column(String(255), nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    uploader = relationship("User")

class Dinosaur(Base):
    __tablename__ = "dinosaurs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    period = Column(String(50))
    diet = Column(String(20))
    length_m = Column(String(10))
    description = Column(Text)
    fun_fact = Column(Text)
    image_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("QuizQuestion", back_populates="dinosaur", cascade="all, delete-orphan")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True, index=True)
    dinosaur_id = Column(Integer, ForeignKey("dinosaurs.id"), nullable=False)
    question = Column(Text, nullable=False)
    correct_answer = Column(String(150), nullable=False)
    wrong_answer_1 = Column(String(150), nullable=False)
    wrong_answer_2 = Column(String(150), nullable=False)
    points = Column(Integer, default=10)
    fact = Column(Text)
    difficulty = Column(String(10), default="easy")

    dinosaur = relationship("Dinosaur", back_populates="questions")

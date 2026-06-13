from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Dinosaur(Base):
    __tablename__ = "dinosaurs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    period = Column(String(50))           # Jurásico, Cretácico, etc.
    diet = Column(String(20))             # carnívoro, herbívoro
    length_m = Column(String(10))         # largo en metros
    description = Column(Text)
    fun_fact = Column(Text)
    image_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

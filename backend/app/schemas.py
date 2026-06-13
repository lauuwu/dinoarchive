from pydantic import BaseModel, EmailStr
from typing import Optional
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

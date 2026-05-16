from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageBase(BaseModel):
    role: str
    content: str

class ChatCreate(BaseModel):
    title: str

class ChatMessage(BaseModel):
    chat_id: str
    content: str

class ChatResponse(BaseModel):
    id: str
    title: str
    created_at: datetime

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

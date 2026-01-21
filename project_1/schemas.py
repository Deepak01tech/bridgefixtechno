from  datetime import datetime
from typing import List, Optional
from xmlrpc.client import DateTime
from project_1.database import Base
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    
    name: str
    email: str
    

class UserCreate(UserBase):
    
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserInDB(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


    # description: str | None = None




class PostCreate(BaseModel):
    tags:List[str] = []
    
    title: str
    content: str

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []

    class Config:
        from_attributes = True
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    
    name: str
    email: str
    

class UserCreate(UserBase):
    
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


    # description: str | None = None
 
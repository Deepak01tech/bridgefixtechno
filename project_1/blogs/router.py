from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
)

@router.get("/blogs/", response_model=List[schemas.User])
def read_blogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    blogs = db.query(models.User).offset(skip).limit(limit).all()
    return blogs

@router.post("/blogs/", response_model=schemas.User, dependencies=[Depends(get_current_user)])
def create_blog(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=user.password,  # In a real app, hash the password!
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/blogs/{user_id}", response_model=schemas.User, dependencies=[Depends(get_current_user)])
def read_blog(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/blogs/{user_id}", response_model=schemas.User, dependencies=[Depends(get_current_user)])
def update_blog(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email
    if user.password is not None:
        db_user.hashed_password = user.password  # In a real app, hash the password!
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/blogs/{user_id}", dependencies=[Depends(get_current_user)])
def delete_blog(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}


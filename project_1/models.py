# models.py
# from datetime import datetime
from datetime import datetime, timezone
from xmlrpc.client import DateTime
from typing import List, Optional
from xmlrpc.client import DateTime
from sqlalchemy import Column, Enum, Integer, String
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

    role = Column(Enum("user", "admin"), default="user")

    # posts = relationship("Post", back_populates="owner")
    posts = relationship("Post", back_populates="owner", cascade="all, delete")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(String(255))
    owner_id = Column(Integer, ForeignKey("users.id"))
    # tags = Column(String(255), nullable=False, default="")
    tags = Column(String(255), default="")
 # Comma-separated tags

    owner = relationship("User", back_populates="posts")

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    owner = relationship("User", back_populates="posts")
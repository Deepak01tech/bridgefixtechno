# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Define your database URL using environment variables for security (recommended)
# Format: mysql+pymysql://<username>:<password>@<host>:<port>/<dbname>
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:deepak@localhost:3306/fastapidb")

engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True # Optional: helps manage persistent connections
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

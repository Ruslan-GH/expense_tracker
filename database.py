import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv() # Завантажуємо змінні з .env

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

def init_db():
    # Імпортуємо Base тут, щоб уникнути помилок циклічного імпорту
    from models import Base
    Base.metadata.create_all(bind=engine)
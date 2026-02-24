import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():

    Base.metadata.create_all(engine)

def get_session():
    return SessionLocal()
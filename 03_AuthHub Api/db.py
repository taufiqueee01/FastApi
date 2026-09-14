from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URLL=os.getenv("DATABASE_URL")

if DATABASE_URLL:
    engine=create_engine(DATABASE_URLL)
    
Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()
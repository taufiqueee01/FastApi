from sqlalchemy import select,create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base,sessionmaker

load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("Database not found")

engine=create_engine(DATABASE_URL)
    
sessionlocal=sessionmaker(bind=engine)

db=sessionlocal()
Base=declarative_base()

def get_db():
    try:
        yield db
    finally:
        db.close()
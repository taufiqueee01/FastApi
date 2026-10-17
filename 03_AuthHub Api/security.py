from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


password_hash=PasswordHash.recommended()
def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password):
    return password_hash.verify(password,hashed_password)
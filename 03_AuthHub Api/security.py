from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") 
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY missing from .env")

ALGORITHM = "HS256"


password_hash=PasswordHash.recommended()
def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password):
    return password_hash.verify(password,hashed_password)

def create_access_token(username:str):
    
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    payload = {
        "sub": username,
        "exp": expiry_time
    }
     # It tells that at this time secret key is not none
    assert SECRET_KEY is not None
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

    return token     

def verify_access_token(token:str):
    
    assert SECRET_KEY is not None
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    
    return payload

def get_username_from_token(token:str):
    
    payload = verify_access_token(token)
    username = payload.get("sub")
    return username

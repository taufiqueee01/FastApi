from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.orm import Session

from pwdlib import PasswordHash
from jose import jwt, JWTError

from dotenv import load_dotenv
import os

from db import get_db
from models import UserModel
from schemas import UserCreate, UserLogin


auth_router = APIRouter()

password_hash = PasswordHash.recommended()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"


# =========================
# REGISTER
# =========================

@auth_router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    result = db.execute(
        select(UserModel).where(
            UserModel.username == user.username
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = password_hash.hash(
        user.password
    )

    new_user = UserModel(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "username": new_user.username
    }


# =========================
# LOGIN
# =========================

@auth_router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    result = db.execute(
        select(UserModel).where(
            UserModel.username == user.username
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not password_hash.verify(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    token = jwt.encode(
        {
            "sub": str(existing_user.id),
            "username": existing_user.username
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# TOKEN
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# =========================
# CURRENT USER
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return int(user_id)

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
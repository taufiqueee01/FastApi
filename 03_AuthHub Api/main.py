from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from db import get_db, Base, engine
from models import UserModel
from schemas import UserCreate
from security import hash_password, verify_password 


Base.metadata.create_all(engine)
app = FastAPI()


# 1. User Registration
@app.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    registeration = UserModel(username=user.username,password=hash_password(user.password))

    user_cheak = db.execute(
        select(UserModel).where(
            UserModel.username
            == user.username,  # Ye UserModel.title db ke data se compare krr rha hai
        )
    ).scalar_one_or_none()

    if user_cheak:
        raise HTTPException(
            status_code=400, detail="User already exist, Please log in "
        )

    db.add(registeration)
    db.commit()
    db.refresh(registeration)
    return f"Hey, {user.username} registeration successfully done.."


# 2. Login
@app.post("/auth/login")
def login(user: UserCreate,db: Session = Depends(get_db)):
    
    try:
        
        user_cheak = db.execute(
            select(UserModel).where(
                UserModel.username== user.username  # Ye UserModel.title db ke data se compare krr rha hai
            )
        ).scalar_one_or_none()
        
        
        if user_cheak is None:
            raise HTTPException(
                status_code=401,
                detail="User not found, Please register"
            )
        verify = verify_password(user.password,user_cheak.password) 
        
        if not verify:
            raise HTTPException(
                status_code=401,
                detail="Please enter the correct username or password.."
            )           
        return f"Successfully login as {user.username},{user_cheak.password}"
    
    except Exception:
        db.rollback()
        raise



# 3. Get Current User
@app.get("/users/me")
def get_current_user():
    pass


# 4. Protected Route
@app.get("/users/protected")
def protected_route():
    pass


# 5. Admin Route
@app.get("/admin")
def admin_route():
    pass


# 6. User-specific Data
@app.get("/users/{user_id}/data")
def user_data():
    pass


# 7. Logout / Token Handling
@app.post("/auth/logout")
def logout():
    pass

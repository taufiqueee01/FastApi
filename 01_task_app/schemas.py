from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    is_complete: bool = False


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
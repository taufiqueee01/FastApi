from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from db import Base


class UserModel(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String,
        unique=True
    )

    password = Column(
        String
    )


class TaskModel(Base):

    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String
    )

    description = Column(
        String
    )

    is_complete = Column(
        Boolean,
        default=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
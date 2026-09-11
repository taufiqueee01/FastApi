from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine, Base, get_db
from models import TaskModel
from schemas import TaskCreate
from auth import auth_router, get_current_user


# Create database tables
Base.metadata.create_all(engine)


# FastAPI app
app = FastAPI()


# Serve frontend files
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


# -------------------------
# FRONTEND PAGES
# -------------------------

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/login")
def login_page():
    return FileResponse("frontend/login.html")


@app.get("/register")
def register_page():
    return FileResponse("frontend/register.html")


@app.get("/dashboard")
def dashboard_page():
    return FileResponse("frontend/dashboard.html")


# Connect auth routes
app.include_router(auth_router)


# -------------------------
# TASK ROUTES
# -------------------------

@app.get("/view_all")
def view_tasks(
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user)
):
    result = db.execute(
        select(TaskModel).where(
            TaskModel.user_id == user_id
        )
    )

    tasks = result.scalars().all()

    return tasks


@app.get("/view/{task_id}")
def view_one_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user)
):
    result = db.execute(
        select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        )
    )

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.post("/add")
def add_task(
    addTask: TaskCreate,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user)
):
    try:
        task = TaskModel(
            title=addTask.title,
            description=addTask.description,
            is_complete=addTask.is_complete,
            user_id=user_id
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    except Exception:
        db.rollback()
        raise


@app.put("/update/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user)
):
    try:
        result = db.execute(
            select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id
            )
        )

        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        task.title = task_data.title
        task.description = task_data.description
        task.is_complete = task_data.is_complete

        db.commit()
        db.refresh(task)

        return task

    except Exception:
        db.rollback()
        raise


@app.delete("/delete/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user)
):
    try:
        result = db.execute(
            select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id
            )
        )

        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        db.delete(task)
        db.commit()

        return {
            "message": "Task deleted"
        }

    except Exception:
        db.rollback()
        raise
from fastapi import FastAPI,Depends,HTTPException
from db import Base,engine,get_db
from models import ExpenseModel
from schemas import ExpenseCreate
from sqlalchemy.orm import Session
from sqlalchemy import select,update,delete


Base.metadata.create_all(engine)

app = FastAPI()

# 1. Add
@app.post("/expenses/add")
def add_expense(
    expense:ExpenseCreate, 
    db: Session=Depends(get_db)
):
    try:
        
        new_expense =ExpenseModel(
            title=expense.title,
            amount=expense.amount,
            category=expense.category)
        
        Expense_cheak = db.execute(
            select(ExpenseModel).where(
                ExpenseModel.title==expense.title,
                ExpenseModel.amount==expense.amount,
                ExpenseModel.category==expense.category
            )
        ).scalar_one_or_none()
        
        if Expense_cheak:
            raise HTTPException(
                status_code=400,
                detail="Expense already exists.....!"
            )
        
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return new_expense 

    except Exception:
        db.rollback()
        raise
    
        
# 2. Get all
@app.get("/expenses/get_all")
def get_expenses(db: Session = Depends(get_db)):

    expenses=db.execute(
        select(ExpenseModel)
    ).scalars().all()

    return expenses
    
    
    


# 3. Get one
@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int,db: Session=Depends(get_db)):
    
    try:
    
        expense=db.execute(select(ExpenseModel).where(
            ExpenseModel.id==expense_id
        )).scalar_one_or_none()
        return expense

    except Exception:
        db.rollback()
        raise


# 4. Update
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int,expense:ExpenseCreate,db:Session=Depends(get_db)):
    
    try:
        
        db.execute(update(ExpenseModel)
            .where(ExpenseModel.id==expense_id)
            .values(
                title=expense.title,
                amount=expense.amount,
                category=expense.category
            )
        )
        
        # Yaha refress use nhi hua beacause we havent fetch any data from the database
        
        db.commit()
        return expense
        
    except Exception:
        db.rollback()
        raise


# 5. Delete
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int,db:Session=Depends(get_db)):
   
   try:
       
    db.execute(delete(ExpenseModel).where(
        ExpenseModel.id==expense_id
    )).scalar_one_or_none()
    
    db.commit()
    
   except Exception:
    db.rollback()
    raise
       

# 6. Category filter
@app.get("/expenses/filter")
def filter_expenses(category: str):
    pass


# 7. Amount filter
@app.get("/expenses/amount")
def filter_by_amount(
    min_amount: int,
    max_amount: int
):
    pass


# 8. Total spending
@app.get("/expenses/total")
def total_spending():
    pass


# 9. Category summary
@app.get("/expenses/summary")
def category_summary():
    pass


# 10. Sorting
@app.get("/expenses/sort")
def sort_expenses(sort: str):
    pass


# 11. Pagination
@app.get("/expenses/page")
def paginate_expenses(
    page: int,
    limit: int
):
    pass
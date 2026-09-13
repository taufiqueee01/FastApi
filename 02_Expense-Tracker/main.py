from fastapi import FastAPI,Depends,HTTPException
from db import Base,engine,get_db
from models import ExpenseModel
from schemas import ExpenseCreate
from sqlalchemy.orm import Session
from sqlalchemy import select,update,delete,func


Base.metadata.create_all(engine)

app = FastAPI()

# 1. Add
@app.post("/expenses/add")
def add_expense(
    expenses:list[ExpenseCreate], # Ye Postmaster se data le raha hai & ye Data validating kar rha hai e & Ye object ki list de rha hai...
    # ExpenseCreate(title="Pizza", amount=300, category="Food"),
    # This is in json format by automatically , pydantic
    db: Session=Depends(get_db)
):
    try:
        
        for expense in expenses:
            new_expense =ExpenseModel(
                title=expense.title.lower(),
                amount=expense.amount,
                category=expense.category.lower())
            
            Expense_cheak = db.execute(
                select(ExpenseModel).where(
                    ExpenseModel.title==expense.title.lower(),  # Ye expensemodel.title db ke data se compare krr rha hai 
                    ExpenseModel.amount==expense.amount,
                    ExpenseModel.category==expense.category.lower()
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

        return {"Status : Expenses add successfully"}

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
    
    
    
# 6. Category filter  # We have put this here because static(/expense/filter) route is always above 
# from dynamic(/static/{expense_id}) , But the same https method like both get or both post
@app.get("/expenses/filter")
def filter_expenses(category: str,db:Session=Depends(get_db)):

    expense=db.execute(select(ExpenseModel).where(ExpenseModel.category==category.lower())).scalars().all()

    return expense

# 7. Amount filter
@app.get("/expenses/amount")
def filter_by_amount(
    min_amount: int,
    max_amount: int,  
    db:Session=Depends(get_db)
):
    
    expense=db.execute(select(ExpenseModel).where(
        ExpenseModel.amount > min_amount,
        ExpenseModel.amount < max_amount)).scalars().all()

    return expense

# 8. Total spending
@app.get("/expenses/total")
def total_spending(db:Session=Depends(get_db)):

    total_spending=db.execute(func.sum(ExpenseModel.amount)).scalar_one()
    return f"Total spending is '{total_spending}'.."


# 9. Category summary
@app.get("/expenses/summary")
def category_summary(db: Session = Depends(get_db)):
    
    summary = db.execute(
        select(
            ExpenseModel.category,
            func.sum(ExpenseModel.amount)
        )
        .group_by(ExpenseModel.category)
    )

    return summary.mappings().all()




# 10. Sorting
@app.get("/expenses/sort")
def sort_expenses(sort: str,db:Session=Depends(get_db)):
    
    if sort == "asc":
        
        Asc_sort=db.execute(select(ExpenseModel).order_by(ExpenseModel.amount.asc())).scalars().all()
        return Asc_sort
    
    elif sort == "desc":
        
        Dec_sort= db.execute(select(ExpenseModel)
            .order_by(ExpenseModel.amount.desc())
            ).scalars().all()
        
        return Dec_sort
        
    else:
        raise HTTPException(
            status_code=400,
            detail="sort must be 'asc' or 'desc'"
        )   
        

# 11. Pagination
@app.get("/expenses/page")
def paginate_expenses(
    page: int,
    limit: int,
    db:Session=Depends(get_db)
):
    offset=(page-1) * limit
    
    Page=db.execute(select(ExpenseModel).offset(offset).limit(limit)).scalars().all()
    return Page


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
    
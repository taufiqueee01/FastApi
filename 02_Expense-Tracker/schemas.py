from pydantic import BaseModel

# It cheaks wheather a data as input is in correct form or not...

class ExpenseCreate(BaseModel):
    title: str
    amount: int
    category: str
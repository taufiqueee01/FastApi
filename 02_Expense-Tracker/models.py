from db import Base
from sqlalchemy import Column,Integer,String

# Ye models structure deta hai ki data kaisa rahega 
# and main.py me by db.add(....) se ham data add krte hai expese model me
 
class ExpenseModel(Base):
    __tablename__="expenses"

    id=Column(Integer,primary_key=True)
    title=Column(String)
    amount=Column(Integer)
    category=Column(String)

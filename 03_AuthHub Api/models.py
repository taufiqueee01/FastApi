from db import Base
from sqlalchemy import Integer,String,Column

class UserModel(Base):
    
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    username=Column(String)
    password=Column(String)


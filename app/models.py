from .database import Base
from sqlalchemy import Column,Integer,String
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)

# Users  model

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    email= Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)


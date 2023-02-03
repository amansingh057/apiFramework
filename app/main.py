from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException,Depends

from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import  models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Posts(BaseModel):
    title: str
    content: str
    # id:int

while True : 

    try:
        conn = psycopg2.connect(host='localhost',database='apidatabase',user='postgres',password='password',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to database !!!!")
        break
    except Exception as error:
        print("FAILED!!!")
        print("Error",error)
        time.sleep(3)

@app.get("/")
def login():
    return {"message": "Welcome to API"}


@app.get("/posts")
def posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Posts,db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response,db: Session = Depends(get_db)):
    post= db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="page not found")

    return {"Post detail": post}

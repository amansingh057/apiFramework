from typing import Optional,List
from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import  models,schemas,utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI()




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


app.include_router(post.router) #Getpost
app.include_router(user.router) #SIGNUP
app.include_router(auth.router) #LOGIN

@app.get("/")
def login():
    return {"message": "Welcome to API"}
from typing import List
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.ResponsePost])
def posts(db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_curr_user)):
    
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.ResponsePost)
def create_post(post: schemas.CreatePost,db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_curr_user)):

    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.ResponsePost)
def get_post(id: int, response: Response,db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_curr_user)):
    post= db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="page not found")

    return post
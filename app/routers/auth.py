from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    tags=['Auth']
)

@router.get("/login",response_model=schemas.Token)
def login(credentials:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    if not utils.verify(credentials.password,user.password) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    #creating Token
    acess_token = oauth2.create_token(data={"user_id":user.id})
    #returning token
    return{"access_token":acess_token,"token_type":"bearer"}
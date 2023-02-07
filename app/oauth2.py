from jose import JWTError, jwt
from datetime import datetime ,timedelta
from . import schemas
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Secret key
# Algorithm
#Expiration time

SECRET_KEY = "vgbhweq8yhoiw;l,qs./;,LXNHIOJPERFV,MVEROPKVBREMKPIEWFKML,;CFCEWRJIOMPFL45678YVGE3DFVG7EGYZSEXDCFVGZA"
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTE = 60

def create_token(data:dict):
    encoding = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTE)
    encoding.update({"exp":expire})

    encoded_jwt=  jwt.encode(encoding,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,cred_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id:str = payload.get("user_id")

        if id is None:
            raise cred_exception

        token_data =schemas.TokenData(id=id)
    except JWTError:
        raise cred_exception

    return token_data

def get_curr_user(token:str = Depends(oauth_scheme)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate user",headers={"WWW-Authenticate": "Bearer"})

    return verify_token(token,cred_exception)


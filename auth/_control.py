from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config.db.connection import db_api
import os

from models._classes import FindAPIUser,APITokenData

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define the superadmin password
SUPERADMIN_PASSWORD = "a2jsKls2?a-s2jab2s2kks"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    user_dict = db_api.users.find_one({"username": username})
    user_dict['_id'] = str(user_dict['_id'])
    if user_dict:
        return user_dict
    
def authenticate_user(username: str, password: str):
    user_dict = db_api.users.find_one({"username": username})
    user_dict['_id'] = str(user_dict['_id'])
    if not user_dict:
        return False
    hashed_password = get_password_hash(password)
    if not verify_password(password, hashed_password):
        return False
    return user_dict

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = APITokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    user = FindAPIUser(**current_user)
    if user.disabled:
        raise HTTPException(status_code=400, detail="Your user is currently inactive. Contact with support")
    return current_user

async def get_support_team(current_user: dict = Depends(get_current_user)):
    user = FindAPIUser(**current_user)
    if not user.softcamp_team:
        raise HTTPException(status_code=400, detail="Yo've not got enough permissions to do that!")
    return current_user


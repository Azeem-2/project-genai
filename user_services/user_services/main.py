from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from user_services.db import create_db_and_tables, get_session
from user_services.schemas import UserCreate, UserRead, TokenResponse, UserDataCreate, UserDataRead
from user_services.crud import create_user, get_user_by_email, authenticate_user, create_user_data, get_user_data
from user_services.auth import create_access_token
from user_services.dp import get_current_user
from user_services.models import User, UserData
from contextlib import asynccontextmanager




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
   

app = FastAPI(lifespan=lifespan)

@app.post("/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(session=db, user=user)

@app.post("/token", response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = authenticate_user(session=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/data", response_model=UserDataRead)
def create_user_data_endpoint(data: UserDataCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return create_user_data(session=db, data=data, user=current_user)

@app.get("/data", response_model=List[UserDataRead])
def read_user_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return get_user_data(session=db, user=current_user)








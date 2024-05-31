from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from user_services.db import create_db_and_tables, get_session
from user_services.schemas import UserCreate, UserRead, TokenResponse, UserDataCreate, UserDataRead, TokenData
from user_services.crud import create_user, get_user_by_email, authenticate_user, create_user_data, get_user_data, refresh_access_token
from user_services.auth import create_access_token
from user_services.dp import get_current_user
from user_services.models import User, UserData
from contextlib import asynccontextmanager
from user_services.crud import validate_password
from slowapi import Limiter
from slowapi.util import get_remote_address
from user_services.kafka.producer import KafkaProducer, get_kafka_producer
from user_services.kafka import _pb2
from typing import List
import asyncio
from user_services.kafka.consumer import run_consumer

limiter = Limiter(key_func=get_remote_address)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    # Start Kafka consumer as a background task
    consumer_task = asyncio.create_task(run_consumer())
    yield
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

@app.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(get_session), producer: KafkaProducer = Depends(get_kafka_producer)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not validate_password(user.password):
        raise HTTPException(status_code=400, detail="Password does not meet criteria")
    new_user = create_user(session=db, user=user)
    user_registered = _pb2.UserRegistered(email=new_user.email, password=user.password)
    await producer.send("user-registered", user_registered)
    return new_user

@app.post("/token", response_model=TokenResponse)
@limiter.limit("5 per minute")
def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = authenticate_user(session=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/refresh", response_model=TokenResponse)
def refresh_token(token: TokenData, db: Session = Depends(get_session)):
    new_token = refresh_access_token(token=token.access_token, db=db)
    if not new_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    return {"access_token": new_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/data", response_model=UserDataRead)
def create_user_data_endpoint(data: UserDataCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return create_user_data(session=db, data=data, user=current_user)

@app.get("/data", response_model=List[UserDataRead])
def read_user_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return get_user_data(session=db, user=current_user)

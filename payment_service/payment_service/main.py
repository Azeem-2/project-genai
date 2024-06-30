from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from payment_service import schemas, crud
from payment_service.db import create_db_and_tables, get_session
from payment_service.schemas import PaymentCreate, PaymentResponse, PaymentList, PaymentDetail
from typing import List
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        yield
    finally:
        pass

app: FastAPI = FastAPI(lifespan=lifespan)


@app.post("/payment", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_session)):
    return crud.create_payment(db, payment)

@app.get("/payment", response_model=List[PaymentList])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud.get_payments(db, skip, limit)

@app.get("/payment/{payment_id}", response_model=PaymentDetail)
def get_payment_by_id(payment_id: int, db: Session = Depends(get_session)):
    return crud.get_payment_by_id(db, payment_id)

@app.put("/payment/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentCreate, db: Session = Depends(get_session)):
    return crud.update_payment(db, payment_id, payment)

@app.delete("/payment/{payment_id}", response_model=PaymentResponse)
def delete_payment(payment_id: int, db: Session = Depends(get_session)):
    return crud.delete_payment(db, payment_id)

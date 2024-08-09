from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel
from payment_service import schemas, crud
from payment_service.db import create_db_and_tables, get_session
from payment_service.schemas import PaymentCreate, PaymentResponse, PaymentList, PaymentDetail
from payment_service.kafka.producer import KafkaProducer, get_kafka_producer
from payment_service.kafka import payment_pb2
from typing import List
from contextlib import asynccontextmanager
import stripe
from payment_service.settings import STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET, STRIPE_PUBLISHABLE_KEY
from fastapi.requests import Request


# Set your Stripe secret key from the settings module
stripe.api_key = str(STRIPE_API_KEY)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()  # Ensure tables are created
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan)







@app.post("/payment", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, db: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    try:
        # Create a payment intent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),  # Stripe expects amount in cents
            currency='usd',
            metadata={'order_id': payment.order_id},
            automatic_payment_methods={'enabled': True}
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Create a payment record in the database
    db_payment = crud.create_payment(db, payment)

    # Assign the client_secret to the payment record
    db_payment.client_secret = intent.client_secret

    # Send a Kafka message
    payment_message = payment_pb2.PaymentCreate(
        order_id=db_payment.order_id,
        amount=db_payment.amount,
        status=db_payment.status
    )
    await kafka_producer.send("payment", payment_message)

    return db_payment




@app.get("/payment", response_model=List[PaymentList])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud.get_payments(db, skip, limit)

@app.get("/payment/{payment_id}", response_model=PaymentDetail)
def get_payment_by_id(payment_id: int, db: Session = Depends(get_session)):
    payment = crud.get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.put("/payment/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: int, payment: PaymentCreate, db: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    updated_payment = crud.update_payment(db, payment_id, payment)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment_message = payment_pb2.PaymentCreate(
        order_id=updated_payment.order_id,
        amount=updated_payment.amount,
        status=updated_payment.status
    )
    await kafka_producer.send("payment", payment_message)
    return updated_payment

@app.delete("/payment/{payment_id}", response_model=PaymentResponse)
async def delete_payment(payment_id: int, db: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    deleted_payment = crud.delete_payment(db, payment_id)
    if not deleted_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment_message = payment_pb2.PaymentCreate(
        order_id=deleted_payment.order_id,
        amount=deleted_payment.amount,
        status=deleted_payment.status
    )
    await kafka_producer.send("payment", payment_message)
    return deleted_payment

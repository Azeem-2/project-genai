from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from order_service import schemas, crud
from order_service.db import create_db_and_tables, get_session
from order_service.kafka.producer import get_kafka_producer
from order_service.kafka.consumer import start_consumer
from order_service.kafka import order_pb2
from typing import List
from contextlib import asynccontextmanager
import asyncio

from order_service.schemas import OrderCreate
from order_service.kafka.producer import KafkaProducer

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        asyncio.create_task(start_consumer())  # Start the consumer task
        yield
    finally:
        pass

app: FastAPI = FastAPI(lifespan=lifespan)

@app.post("/orders/")
async def create_order(order: OrderCreate, kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    order_message = order_pb2.OrderCreate(
        user_id=order.user_id,
        items=[order_pb2.Item(product_id=item.product_id, quantity=item.quantity) for item in order.items],
        total_price=order.total_price
    )
    await kafka_producer.send("orders", order_message)
    return {"status": "Order sent to Kafka"}

@app.get("/order", response_model=List[schemas.OrderList])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud.get_orders(db, skip, limit)

@app.get("/order/{order_id}", response_model=schemas.OrderDetail)
def get_order_by_id(order_id: int, db: Session = Depends(get_session)):
    return crud.get_order_by_id(db, order_id)

@app.put("/order/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_session)):
    return crud.update_order(db, order_id, order)

@app.delete("/order/{order_id}", response_model=schemas.OrderResponse)
def delete_order(order_id: int, order: schemas.OrderDelete, db: Session = Depends(get_session)):
    return crud.delete_order(db, order_id)

@app.get("/order/{order_id}/items", response_model=List[schemas.OrderItemBase])
def get_order_items(order_id: int, db: Session = Depends(get_session)):
    return crud.get_order_items(db, order_id)

@app.get("/order/{order_id}/items/{item_id}", response_model=schemas.OrderItemBase)
def get_order_item_by_id(order_id: int, item_id: int, db: Session = Depends(get_session)):
    return crud.get_order_item_by_id(db, order_id, item_id)

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from order_service import schemas, crud
from order_service.db import create_db_and_tables, get_session
from order_service.kafka.producer import get_kafka_producer, KafkaProducer
from order_service.kafka.consumer import start_consumer
from order_service.kafka import order_pb2
from typing import List
from contextlib import asynccontextmanager
import asyncio

from order_service.schemas import OrderCreate, OrderUpdate, OrderItemUpdate

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
async def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    updated_order = crud.update_order(db, order_id, order)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    order_message = order_pb2.OrderUpdate(
        id=updated_order.id,
        user_id=updated_order.user_id,
        items=[order_pb2.Item(product_id=item.product_id, quantity=item.quantity) for item in order.items],
        total_price=updated_order.total_price
    )
    await kafka_producer.send("orders", order_message)
    return updated_order

@app.delete("/order/{order_id}", response_model=schemas.OrderResponse)
async def delete_order(order_id: int, db: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    deleted_order = crud.delete_order(db, order_id)
    if deleted_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    order_message = order_pb2.OrderDelete(
        id=deleted_order.id,
        user_id=deleted_order.user_id
    )
    await kafka_producer.send("orders", order_message)
    return deleted_order

@app.get("/order/{order_id}/items", response_model=List[schemas.OrderItemBase])
def get_order_items(order_id: int, db: Session = Depends(get_session)):
    return crud.get_order_items(db, order_id)

@app.get("/order/{order_id}/items/{item_id}", response_model=schemas.OrderItemBase)
def get_order_item_by_id(order_id: int, item_id: int, db: Session = Depends(get_session)):
    return crud.get_order_item_by_id(db, order_id, item_id)

@app.put("/order/{order_id}/items/{item_id}", response_model=schemas.OrderItemBase)
async def update_order_item(order_id: int, item_id: int, item: OrderItemUpdate, db: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    updated_item = crud.update_order_item(db, order_id, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")

    item_message = order_pb2.OrderItemUpdate(
        id=updated_item.id,
        order_id=updated_item.order_id,
        product_id=updated_item.product_id,
        quantity=updated_item.quantity
    )
    await kafka_producer.send("order_items", item_message)
    return updated_item

@app.delete("/order/{order_id}/items/{item_id}", response_model=schemas.OrderItemBase)
async def delete_order_item(order_id: int, item_id: int, db: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    deleted_item = crud.delete_order_item(db, order_id, item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")

    item_message = order_pb2.OrderItemDelete(
        id=deleted_item.id,
        order_id=deleted_item.order_id
    )
    await kafka_producer.send("order_items", item_message)
    return deleted_item

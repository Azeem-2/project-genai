from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from inventory_service import schemas, crud
from inventory_service.db import create_db_and_tables, get_session
from inventory_service.kafka.producer import get_kafka_producer
from inventory_service.kafka.consumer import start_consumer
from inventory_service.kafka import inventory_pb2
from typing import List
from contextlib import asynccontextmanager
import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka import AIOKafkaConsumer
from inventory_service.kafka.producer import KafkaProducer  # Correct import


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        asyncio.create_task(start_consumer())  # Start the consumer task
        yield
    finally:
        pass

app: FastAPI = FastAPI(lifespan=lifespan)

@app.post("/inventory/", response_model=schemas.InventoryItemRead)
async def create_inventory_item(item: schemas.InventoryItemCreate, db: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    # Create item in database
    db_item = crud.create_inventory_item(db, item)

    # Create and serialize inventory message
    inventory_message = inventory_pb2.InventoryUpdate(
        product_id=item.product_id,
        quantity=item.quantity
    )
    await kafka_producer.send("inventory", inventory_message)

    return db_item  # Return the created item


@app.get("/inventory", response_model=List[schemas.InventoryItemRead])
def get_inventory_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud.get_inventory_items(db, skip, limit)

@app.get("/inventory/{item_id}", response_model=schemas.InventoryItemRead)
def get_inventory_item_by_id(item_id: int, db: Session = Depends(get_session)):
    return crud.get_inventory_item(db, item_id)

@app.put("/inventory/{item_id}", response_model=schemas.InventoryItemRead)
def update_inventory_item(item_id: int, item: schemas.InventoryItemUpdate, db: Session = Depends(get_session)):
    return crud.update_inventory_item(db, item_id, item)

@app.delete("/inventory/{item_id}", response_model=dict)
def delete_inventory_item(item_id: int, db: Session = Depends(get_session)):
    result = crud.delete_inventory_item(db, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from product_service.db import create_db_and_tables, get_session
from product_service.schemas import ProductCreate, ProductRead
from product_service.crud import create_product, get_product_by_id, get_products
from product_service.kafka.producer import KafkaProducer, get_kafka_producer
from product_service.kafka import _pb2
from typing import List
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/products/", response_model=ProductRead)
async def create_new_product(product: ProductCreate, db: Session = Depends(get_session), producer: KafkaProducer = Depends(get_kafka_producer)):
    db_product = create_product(session=db, product=product)
    product_registered = _pb2.ProductRegistered(
        product_id=db_product.id, 
        name=db_product.name, 
        price=db_product.price
    )
    await producer.send("product-registered", product_registered)
    return db_product

@app.get("/products/{product_id}", response_model=ProductRead)
def read_product(product_id: int, db: Session = Depends(get_session)):
    db_product = get_product_by_id(session=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/", response_model=List[ProductRead])
def read_products(db: Session = Depends(get_session)):
    return get_products(session=db)

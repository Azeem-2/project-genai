import asyncio
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session
from product_service.crud import get_product_by_id  # Example of a CRUD function you might need
from product_service.db import engine
from product_service.kafka import _pb2

KAFKA_BROKER_URL = "broker:19092"
PRODUCT_TOPIC = "product-registered"

class KafkaConsumer:
    def __init__(self, broker_url: str, topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=broker_url,
            group_id="product_group",
            auto_offset_reset="earliest"
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def consume(self):
        await self.start()
        try:
            async for msg in self.consumer:
                product_registered = _pb2.ProductRegistered()
                product_registered.ParseFromString(msg.value)
                session = Session(engine)
                try:
                    # Handle the message (example: log product details)
                    print(f"Product Registered: {product_registered.product_id}, Name: {product_registered.name}, Price: {product_registered.price}")
                finally:
                    session.close()
        finally:
            await self.stop()

async def run_consumer():
    consumer = KafkaConsumer(KAFKA_BROKER_URL, PRODUCT_TOPIC)
    await consumer.consume()

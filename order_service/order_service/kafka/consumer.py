import asyncio
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session
from order_service.crud import create_order
from order_service.db import get_session
from order_service.kafka import order_pb2
from order_service.schemas import OrderCreate

KAFKA_BROKER_URL = "broker:19092"
ORDER_TOPIC = "orders"

class KafkaConsumer:
    def __init__(self, broker_url: str, topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=broker_url,
            group_id="order_group",
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
                order_data = order_pb2.OrderCreate()
                order_data.ParseFromString(msg.value)
                order_dict = {
                    "user_id": order_data.user_id,
                    "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in order_data.items],
                    "total_price": order_data.total_price
                }
                async with get_session() as session:
                    create_order(session, OrderCreate(**order_dict))
        except Exception as e:
            print(f"Failed to consume message from Kafka: {e}")
        finally:
            await self.stop()

async def start_consumer():
    consumer = KafkaConsumer(KAFKA_BROKER_URL, ORDER_TOPIC)
    await consumer.consume()

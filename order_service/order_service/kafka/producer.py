from aiokafka import AIOKafkaProducer
import asyncio
from order_service.kafka import order_pb2
from typing import AsyncGenerator

KAFKA_BROKER_URL = "broker:19092"
ORDER_TOPIC = "orders"

class KafkaProducer:
    def __init__(self, broker_url: str):
        self.producer = AIOKafkaProducer(bootstrap_servers=broker_url)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic: str, message: order_pb2.OrderCreate):
        try:
            await self.producer.send_and_wait(topic, message.SerializeToString())
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")

async def get_kafka_producer() -> AsyncGenerator[KafkaProducer, None]:
    producer = KafkaProducer(KAFKA_BROKER_URL)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

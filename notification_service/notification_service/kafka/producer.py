# producer.py
from aiokafka import AIOKafkaProducer
import asyncio
from notification_service.kafka import notification_pb2

KAFKA_BROKER_URL = "broker:19092"
NOTIFICATION_TOPIC = "notification"

class KafkaProducer:
    def __init__(self, broker_url: str):
        self.producer = AIOKafkaProducer(bootstrap_servers=broker_url)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic: str, message: notification_pb2.NotificationCreate):
        serialized_message = message.SerializeToString()
        await self.producer.send_and_wait(topic, serialized_message)

async def get_kafka_producer():
    producer = KafkaProducer(KAFKA_BROKER_URL)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

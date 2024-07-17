import asyncio
from aiokafka import AIOKafkaConsumer
from user_services.kafka import _pb2
from sqlmodel import Session
from user_services.models import User
from user_services.db import engine

KAFKA_BROKER_URL = "broker:19092"
USER_TOPIC = "user-registered"

class KafkaConsumer:
    def __init__(self, broker_url: str, topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=broker_url,
            group_id="user_group",
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
                user = _pb2.UserRegistered()
                user.ParseFromString(msg.value)
                with Session(engine) as session:
                    try:
                        db_user = User(email=user.email, password=user.password)
                        session.add(db_user)
                        session.commit()
                    except Exception as e:
                        session.rollback()
                        raise e
        finally:
            await self.stop()

async def run_consumer():
    consumer = KafkaConsumer(KAFKA_BROKER_URL, USER_TOPIC)
    await consumer.consume()

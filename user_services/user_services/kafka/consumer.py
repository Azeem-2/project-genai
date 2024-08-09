import asyncio
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session
from user_services.crud import create_user  # Adjust based on actual CRUD function needed
from user_services.db import engine
from user_services.kafka import _pb2

KAFKA_BROKER_URL = "broker:19092"
USER_TOPIC = "user-registered"  # Topic name for user registration

class KafkaConsumer:
    def __init__(self, broker_url: str, topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=broker_url,
            group_id="user_group",  # Group ID for user registration
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
                user_registered = _pb2.UserRegistered()
                user_registered.ParseFromString(msg.value)
                session = Session(engine)
                try:
                    # Handle the message (example: log user details)
                    print(f"User Registered: User ID: {user_registered.user_id}, Email: {user_registered.email}")
                    # Add any further processing needed, like saving to a database
                    # For example: create_user(session, user_registered) if you have such a function
                finally:
                    session.close()
        finally:
            await self.stop()

async def run_consumer():
    consumer = KafkaConsumer(KAFKA_BROKER_URL, USER_TOPIC)
    await consumer.consume()

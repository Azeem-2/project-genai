import asyncio
from aiokafka import AIOKafkaConsumer
from user_services.kafka import _pb2
from user_services.db import get_session
from user_services.models import User
from user_services.auth import get_password_hash

class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id="my-group"
        )

    async def start(self):
        await self.consumer.start()

    async def consume(self):
        async for msg in self.consumer:
            session = next(get_session())
            try:
                # Deserialize message from binary format using Protobuf
                user_registered = _pb2.UserRegistered()
                user_registered.ParseFromString(msg.value)
                print(f"Consumed message: {user_registered}")
                
                # Add user to the database
                hashed_password = get_password_hash(user_registered.password)
                db_user = User(email=user_registered.email, hashed_password=hashed_password)
                session.add(db_user)
                session.commit()
                session.refresh(db_user)
            except Exception as e:
                session.rollback()
                print(f"Error processing message: {e}")
            finally:
                session.close()

    async def stop(self):
        await self.consumer.stop()

async def run_consumer():
    consumer = KafkaConsumer(bootstrap_servers='broker:19092', topic='user-registered')
    await consumer.start()
    try:
        await consumer.consume()
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(run_consumer())

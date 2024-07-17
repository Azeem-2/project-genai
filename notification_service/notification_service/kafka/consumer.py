import asyncio
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session
from notification_service import crud, db, notification_pb2

KAFKA_BROKER_URL = "broker:19092"
NOTIFICATION_TOPIC = "notification"

class KafkaConsumer:
    def __init__(self, broker_url: str, topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=broker_url,
            group_id="notification_group",
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
                notification_create = notification_pb2.NotificationCreate()
                # Ensure correct deserialization
                notification_create.ParseFromString(msg.value)
                session = Session(db.engine)  # Create session inside the loop
                try:
                    # Create the notification using the correct deserialized data
                    crud.create_notification(notification_create, session)
                finally:
                    session.close()  # Close session after each message processing
        finally:
            await self.stop()

async def start_consumer():
    consumer = KafkaConsumer(KAFKA_BROKER_URL, NOTIFICATION_TOPIC)
    await consumer.consume()

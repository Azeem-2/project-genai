import asyncio
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session
from payment_service.db import get_session, engine
from payment_service.crud import update_payment_status
from payment_service.kafka import payment_pb2

KAFKA_BROKER_URL = "broker:19092"
PAYMENT_TOPIC = "payment"

class KafkaConsumer:
    def __init__(self, broker_url: str, topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=broker_url,
            group_id="payment_group",
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
                payment_message = payment_pb2.PaymentCreate()
                payment_message.ParseFromString(msg.value)
                session = Session(engine)  # Create session inside the loop
                try:
                    # Update payment status using the correct deserialized data
                    update_payment_status(session, payment_message.order_id, payment_message.status)
                finally:
                    session.close()  # Close session after each message processing
        finally:
            await self.stop()

async def start_consumer():
    consumer = KafkaConsumer(KAFKA_BROKER_URL, PAYMENT_TOPIC)
    await consumer.consume()

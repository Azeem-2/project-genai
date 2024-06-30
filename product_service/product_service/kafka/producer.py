import asyncio
import logging
from aiokafka import AIOKafkaProducer
from product_service.kafka import _pb2
from typing import AsyncGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)

    async def start(self):
        await self.producer.start()
        logger.info("Kafka producer started.")

    async def send(self, topic: str, message):
        try:
            # Serialize message to binary format using Protobuf
            await self.producer.send_and_wait(topic, message.SerializeToString())
            logger.info(f"Message sent to topic '{topic}': {message}")
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {e}")

    async def stop(self):
        await self.producer.stop()
        logger.info("Kafka producer stopped.")

async def get_kafka_producer() -> AsyncGenerator[KafkaProducer, None]:
    producer = KafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

if __name__ == "__main__":
    async def test_producer():
        async with get_kafka_producer() as producer:
            # Example test message
            message = _pb2.ProductRegistered(
                product_id=1,
                name="Test Product",
                price=10.99
            )
            await producer.send("product-registered", message)

    asyncio.run(test_producer())

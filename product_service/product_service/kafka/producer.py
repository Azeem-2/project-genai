import asyncio
from aiokafka import AIOKafkaProducer
from product_service.kafka import _pb2
from typing import AsyncGenerator

class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def send(self, topic: str, message):
        # Serialize message to binary format using Protobuf
        await self.producer.send_and_wait(topic, message.SerializeToString())
        print(f"Message sent to topic '{topic}': {message}")

    async def stop(self):
        await self.producer.stop()

async def get_kafka_producer() -> AsyncGenerator[KafkaProducer, None]:
    producer = KafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

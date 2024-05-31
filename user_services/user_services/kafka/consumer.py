import asyncio
from aiokafka import AIOKafkaConsumer
from google.protobuf.json_format import Parse
from user_services.kafka import _pb2

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
            # Deserialize message from binary format using Protobuf
            user_registered = _pb2.UserRegistered()
            user_registered.ParseFromString(msg.value)
            print(f"Consumed message: {user_registered}")

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

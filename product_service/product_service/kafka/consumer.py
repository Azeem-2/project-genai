import asyncio
from aiokafka import AIOKafkaConsumer

async def run_consumer():
    consumer = AIOKafkaConsumer(
        'product-registered',
        bootstrap_servers='broker:19092',
        group_id="product_group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Consumed message from topic 'product-registered': {msg.value}")
    finally:
        await consumer.stop()

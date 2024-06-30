import asyncio
import logging
from aiokafka import AIOKafkaConsumer, ConsumerStoppedError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_consumer():
    consumer = AIOKafkaConsumer(
        'product-registered',
        bootstrap_servers='broker:19092',
        group_id="product_group",
        auto_offset_reset='earliest'
    )

    await consumer.start()
    try:
        async for msg in consumer:
            logger.info(f"Consumed message from topic 'product-registered': {msg.value.decode('utf-8')}")
    except ConsumerStoppedError:
        logger.warning("Consumer stopped unexpectedly.")
    except Exception as e:
        logger.error(f"Error in consumer: {e}")
    finally:
        await consumer.stop()
        logger.info("Consumer stopped.")

if __name__ == "__main__":
    asyncio.run(run_consumer())

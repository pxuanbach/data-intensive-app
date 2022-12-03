import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from config import settings


loop = asyncio.get_event_loop()
aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.KAFKA_INSTANCE)
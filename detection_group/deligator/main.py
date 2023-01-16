from typing import Any
from fastapi import FastAPI, Body
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from aiokafka import AIOKafkaConsumer

from logger import logger
from config import settings


loop = asyncio.get_event_loop()
consumer = AIOKafkaConsumer(
    "detect_topic", 
    bootstrap_servers=settings.KAFKA_INSTANCE, 
    loop=loop, 
    auto_offset_reset='earliest', 
    group_id="1",
    enable_auto_commit=False
)


async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
            logger.info(
                f"consumed: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}, {msg.timestamp}"
            )
    finally:
        await consumer.stop()


app = FastAPI(
    title="Detect Group Deligator",
    description="Development",
    version="1.0",
    default_response_class=ORJSONResponse
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    expose_headers=["Content-Range", "Range"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    loop.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()


@app.get("/")
async def root():
    """Health check."""
    # return {"status_code": 200, "detail": "Healthy!"}
    return ORJSONResponse(
        content={"detail": "Healthy!"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8000"),
    )
    
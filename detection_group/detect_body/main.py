import base64
from typing import Any
from fastapi import FastAPI, Body, Depends
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
from PIL import Image
import numpy as np
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, func
import asyncio
from aiokafka import AIOKafkaConsumer
from io import BytesIO
import json

from config import settings
from models import DetectModel
from logger import logger
from db import SessionLocal, async_session_maker
from detector import _detect
from trace_timer import TraceTimer


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal(future=True)
        yield db
    finally:
        if db is not None:
            db.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


loop = asyncio.get_event_loop()
consumer = AIOKafkaConsumer(
    "detect", 
    bootstrap_servers=settings.KAFKA_INSTANCE, 
    loop=loop, 
    auto_offset_reset='earliest', 
    group_id=settings.KAFKA_CONSUMER_GROUP_ID,
    enable_auto_commit=False
)


async def consume():
    # await consumer.start()
    try:
        async for msg in consumer:
            db = SessionLocal(future=True)
            # logger.info(
            #     f"consumed: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}, {msg.timestamp}"
            # )
            timer = TraceTimer(timer_type="performance")
            timer.start()
            try:
                if isinstance(json.loads(msg.value), dict):
                    _data = json.loads(msg.value)
                    img_id = _data["img_id"]
                    decoded = base64.b64decode(_data['bytes'])
                    image = Image.open(BytesIO(decoded))
                    img = np.array(image)
                    result = _detect(img_id, img)
                    db_obj_arr = []
                    for obj in result:
                        if isinstance(obj, dict):
                            db_obj = DetectModel(**obj, img_id=1)
                            db_obj_arr.append(db_obj)
                        else:
                            obj = dict(obj)
                            db_obj = DetectModel(**obj, img_id=2)
                            db_obj_arr.append(db_obj)
                    db.add_all(db_obj_arr)
                    db.commit()
            except Exception as e:
                logger.error(str(e))
            timer.stop()
            logger.debug(f"{msg.topic}_{msg.partition} {msg.offset} Trace time {timer.time_sec} s")
            await consumer.commit()
            # elif isinstance(msg.value, bytes):
            #     image = Image.open(BytesIO(msg.value))
            #     img = np.array(image)
            #     result = _detect(2, img)
            #     db_obj_arr = []
            #     for obj in result:
            #         if isinstance(obj, dict):
            #             db_obj = DetectModel(**obj, img_id=1)
            #             db_obj_arr.append(db_obj)
            #         else:
            #             obj = dict(obj)
            #             db_obj = DetectModel(**obj, img_id=2)
            #             db_obj_arr.append(db_obj)
            #     db.add_all(db_obj_arr)
            #     db.commit()
    finally:
        await consumer.stop()


app = FastAPI(
    title="Detect Body",
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
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    connected = False
    while not connected:
        try:
            await consumer.start()
            connected = True
        except:
            logger.error("Kafka Consumer retry connect")
            await asyncio.sleep(3)
    logger.info("Kafka Consumer connected")
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


@app.get("/detected-result")
async def get_model(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_async_session)
):
    total = await session.scalar(select(func.count(DetectModel.id)))
    result = (
        (
            await session.execute(
                select(DetectModel)
                .offset(skip)
                .limit(limit)
            )
        )
        .scalars()
        .all()
    )
    return {
        "total": total,
        "data": result
    }


@app.post("/detect")
async def detect_face(
    image_url: str = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    res = requests.get(image_url, stream=True)
    if res.status_code == 200:
        image = Image.open(res.raw)
        image.save("./haha.png", quality=95) #quality=95
        img = np.array(image)

        result = _detect(2, img)
        db_obj_arr = []
        for obj in result:
            if isinstance(obj, dict):
                db_obj = DetectModel(**obj, img_id=1)
                db_obj_arr.append(db_obj)
            else:
                obj = dict(obj)
                db_obj = DetectModel(**obj, img_id=2)
                db_obj_arr.append(db_obj)
        session.add_all(db_obj_arr)
        await session.commit()
        return db_obj_arr
    return 


@app.delete("/clear-result")
async def clear_result(
    session: AsyncSession = Depends(get_async_session)
):
    result = (
        (
            await session.execute(
                select(DetectModel)
            )
        )
        .scalars()
        .all()
    )
    for db_obj in result:
        await session.delete(db_obj)
    await session.commit()
    return "Success!"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8000"),
    )
    
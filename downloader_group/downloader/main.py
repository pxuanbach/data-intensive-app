import io
from typing import Any
from fastapi import FastAPI, Body
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from PIL import Image
import requests
import base64

from logger import logger
from trace_timer import TraceTimer
from config import settings
from process_image import process_image_name, process_image, process_url


loop = asyncio.get_event_loop()
aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.KAFKA_INSTANCE)
consumer = AIOKafkaConsumer(
    "test1", 
    bootstrap_servers=settings.KAFKA_INSTANCE, 
    loop=loop, 
    auto_offset_reset="earliest",
    group_id="1",
    enable_auto_commit=False
)


async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
            """
            value = {
                "id": 1, 
                "img_url": "http://localhost:8001/static/image_1.jpg", 
                "done": false
            }
            """
            # print(
            #     "consumed: ",
            #     msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp,
            # )
            timer = TraceTimer(timer_type="performance")
            timer.start()
            try:
                if isinstance(json.loads(msg.value), dict):
                    _data = json.loads(msg.value)
                    img_id = _data["id"]
                    img_url = _data["img_url"]
                    img_url = process_url(img_url)
                    # file_name = process_image_name(img_url)
                    # local_link = process_image(img_url, file_name)
                    res = requests.get(img_url, stream=True)
                    if res.status_code == 200:
                        image = Image.open(res.raw)
                        image.thumbnail((800, 800))
                        timer.stop()
                        logger.debug(f"{msg.topic}_{msg.partition} {msg.offset} {msg.value}")
                        logger.debug(f"{msg.topic}_{msg.partition} {msg.offset} Trace time {timer.time_sec} s")
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format="PNG")
                        img_byte_arr = img_byte_arr.getvalue()
                        encoded = base64.b64encode(img_byte_arr)
                        # logger.info(type(encoded))
                        await aioproducer.send("detect", json.dumps({"img_id": img_id, "bytes": encoded.decode('utf-8')}).encode("ascii"))
            except Exception as e:
                logger.error(str(e))
            await consumer.commit()

    finally:
        await consumer.stop()


app = FastAPI(
    title="Downloader API",
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
    connected = False
    while not connected:
        try:
            await aioproducer.start()
            connected = True
        except:
            logger.error("Kafka Producer retry connect")
            await asyncio.sleep(3)
    logger.info("Kafka Producer connected")
    loop.create_task(consume())
    # connected = False
    # while not connected:
    #     try:
    #         await aioproducer.start()
    #         connected = True
    #     except:
    #         logger.error("Kafka Producer retry connect")
    #         await asyncio.sleep(3)
    # logger.info("Kafka Producer connected")


@app.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()
    await aioproducer.stop()


@app.get("/")
async def root():
    """Health check."""
    # return {"status_code": 200, "detail": "Healthy!"}
    return ORJSONResponse(
        content={"detail": "Healthy!"}
    )


@app.post("/images")
async def get_image_and_save(
    img_url: str = Body(...),
) -> Any:
    # img_url = process_url(img_url)
    # file_name = process_image_name(img_url)
    # local_link = process_image(img_url, file_name)
    logger.info(f"Receive {img_url}")
    return img_url


@app.post("/send_detect")
async def test_send_message(
    topic_name: str = "",
    img_url: str = Body(...),
) -> Any:
    """detect"""
    # for i in range(10):
    #     await aioproducer.send(topic_name, json.dumps({"id": i, "from": settings.SERVER_HOST}).encode("ascii"))
    res = requests.get(img_url, stream=True)
    if res.status_code == 200:
        image = Image.open(res.raw)
        image.thumbnail((800, 800))
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()
        logger.info(type(img_byte_arr))
        await aioproducer.send(topic_name, img_byte_arr)
    return


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8000"),
    )
    
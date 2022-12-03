import time
import calendar
from typing import Any
from fastapi import FastAPI, Body
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import requests
import asyncio
from aiokafka import AIOKafkaConsumer

from config import settings


loop = asyncio.get_event_loop()
consumer = AIOKafkaConsumer("test1", bootstrap_servers=settings.KAFKA_INSTANCE, loop=loop)


async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )

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


@app.post("/images")
async def get_image_and_save(
    img_url: str = Body(...),
) -> Any:
    if img_url.startswith("http://localhost"):
        img_url = img_url.replace("http://localhost", "http://host.docker.internal", 1)
    url_split = img_url.split('/')
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)
    file_name = f"{ts}_{url_split[len(url_split)-1]}"
    try:
        res = requests.get(img_url, stream=True)
        if res.status_code == 200:
            destination_file_path = f"{settings.STATIC_PATH}/{file_name}"
            image = Image.open(res.raw)
            image.thumbnail((800, 800))
            image.save(destination_file_path, quality=95) #quality=95
            return f"{settings.SERVER_HOST}{remove_dot_in_path(destination_file_path)}"
    except Exception as e:
        print(str(e))
    

def remove_dot_in_path(value: str) -> str:
    if value.startswith("."):
        value = value.replace(".", "", 1)
    return value


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8000"),
    )
    
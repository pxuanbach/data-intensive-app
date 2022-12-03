import asyncio
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaProducer

import api
from config import settings
from api.producer import aioproducer


app = FastAPI(
    title="Deligator API",
    description="Development",
    version="1.0",
    default_response_class=ORJSONResponse
)

print(settings.KAFKA_INSTANCE)
# loop = asyncio.get_event_loop()
# aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.KAFKA_INSTANCE)
# aioconsumer = AIOKafkaConsumer("test1", bootstrap_servers=settings.KAFKA_INSTANCE, loop=loop)


@app.on_event("startup")
async def startup_event():
    await aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()


@app.get("/")
async def root():
    """Health check."""
    # return {"status_code": 200, "detail": "Healthy!"}
    return ORJSONResponse(
        content={"detail": "Healthy!"}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    expose_headers=["Content-Range", "Range"],
    allow_headers=["*"],
)
app.include_router(api.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8000"),
    )
    
import asyncio
import json
from typing import Any, List
from pydantic import BaseModel, StrictStr
from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import settings
from deps.db import get_async_session
from models import Image


class ProducerResponse(BaseModel):
    name: StrictStr
    message_id: StrictStr
    topic: StrictStr
    timestamp: StrictStr = ""


class ProducerMessage(BaseModel):
    name: StrictStr
    message_id: StrictStr = ""
    timestamp: StrictStr = ""


class ImageSchema(BaseModel):
    id: int
    img_url: str
    done: bool

    class Config:
        orm_mode = True


router = APIRouter(prefix="/producer")
loop = asyncio.get_event_loop()
aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.KAFKA_INSTANCE)


@router.post("/{topicname}")
async def kafka_produce(msg: ProducerMessage, topicname: str):
    await aioproducer.send(topicname, json.dumps(msg.dict()).encode("ascii"))
    response = ProducerResponse(
        name=msg.name, message_id=msg.message_id, topic=topicname
    )
    return response


@router.post("/start/{topicname}")
async def start_deligate(
    topicname: str,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    images: List[Image] = (
        (
            await session.execute(select(Image))
        )
        .scalars().all()
    )
    await session.commit()
    for obj in images:
        obj = ImageSchema.from_orm(obj)
        await aioproducer.send(topicname, json.dumps(obj.dict()).encode("ascii"))
        await asyncio.sleep(2)
    return "Done!"

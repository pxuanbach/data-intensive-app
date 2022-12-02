import random
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select

from deps.db import get_async_session, get_db
from models import Image


router = APIRouter(prefix="/images")


@router.get("")
async def get_images(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Get all images"""
    images = (
        (
            await session.execute(select(Image))
        )
        .scalars().all()
    )
    return {
        "total": len(images),
        "images": images
    }


@router.post("")
async def insert_images(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Init 1000 image"""
    urls = [
        "http://localhost:8001/static/image_1.jpg",
        "http://localhost:8001/static/image_2.jpg",
        "http://localhost:8001/static/image_3.jpg",
        "http://localhost:8001/static/image_4.jpg",
        "http://localhost:8001/static/image_5.jpg",
    ]
    db_obj_arr = []
    for i in range(0, 1000):
        image = Image(
            img_url=urls[random.randint(0, 4)],
            done=False
        )
        db_obj_arr.append(image)
    session.add_all(db_obj_arr)
    await session.commit()
    return db_obj_arr


@router.delete("")
async def delete_images(
    session: Session = Depends(get_db)
) -> Any:
    """Delete all images"""
    session.query(Image).delete()
    session.commit()
    return "Deleted successfully!"

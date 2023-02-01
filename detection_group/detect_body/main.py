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

from models import DetectBody
from db import SessionLocal, async_session_maker
from detector import _detect

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


app = FastAPI(
    title="Detect Face",
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


@app.get("/")
async def root():
    """Health check."""
    # return {"status_code": 200, "detail": "Healthy!"}
    return ORJSONResponse(
        content={"detail": "Healthy!"}
    )


@app.post("/detect-face")
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
                db_obj = DetectBody(**obj, img_id=1)
                db_obj_arr.append(db_obj)
            else:
                obj = dict(obj)
                db_obj = DetectBody(**obj, img_id=2)
                db_obj_arr.append(db_obj)
        session.add_all(db_obj_arr)
        await session.commit()
        return db_obj_arr
    return 



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8111"),
    )
    
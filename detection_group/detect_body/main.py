from typing import Any
from fastapi import FastAPI, Body
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
from PIL import Image
import numpy as np
import cv2

from detector import _detect


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
    image_url: str = Body(...)
):
    res = requests.get(image_url, stream=True)
    if res.status_code == 200:
        image = Image.open(res.raw)
        image.save("./haha.png", quality=95) #quality=95
        img = np.array(image)

        _detect(img)
    return



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8000"),
    )
    
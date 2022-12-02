from fastapi import APIRouter

from config import settings
from api import init_data


router = APIRouter(prefix=settings.API_PATH)


router.include_router(init_data.router, tags=["images"])

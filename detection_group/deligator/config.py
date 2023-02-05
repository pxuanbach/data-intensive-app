import os
from typing import Any, Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

    API_PATH: str = "/api/v1"
    KAFKA_INSTANCE: str
    KAFKA_CONSUMER_GROUP_ID: str
    LOG_PATH: str = "./static/0logs.log"

settings = Settings()
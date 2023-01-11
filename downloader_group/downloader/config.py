import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    API_PATH: str = "/api/v1"
    STATIC_PATH: str = "./static"
    LOG_PATH: str = "./static/0logs.log"
    SERVER_HOST: str 
    KAFKA_INSTANCE: str
    # KAFKA_INSTANCE = "localhost:9092"

settings = Settings()
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    API_PATH: str = "/api/v1"
    STATIC_PATH: str = "./static"
    SERVER_HOST: str = "localhost:8080"
    KAFKA_INSTANCE = "kafka:9093"
    # KAFKA_INSTANCE = "localhost:9092"

settings = Settings()
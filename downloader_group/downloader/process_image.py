import time
import calendar
from PIL import Image
import requests

from config import settings


def remove_dot_in_path(value: str) -> str:
    if value.startswith("."):
        value = value.replace(".", "", 1)
    return value


def process_url(url: str) -> str:
    if url.startswith("http://localhost"):
        url = url.replace("http://localhost", "http://host.docker.internal", 1)
    return url


def process_image_name(url: str) -> str:
    url_split = url.split('/')
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)
    file_name = f"{ts}_{url_split[len(url_split)-1]}"
    return file_name


def process_image(url: str, file_name: str) -> str:
    try:
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            destination_file_path = f"{settings.STATIC_PATH}/{file_name}"
            image = Image.open(res.raw)
            image.thumbnail((800, 800))
            image.save(destination_file_path, quality=95) #quality=95
            return f"{settings.SERVER_HOST}{remove_dot_in_path(destination_file_path)}"
    except Exception as e:
        print(str(e))
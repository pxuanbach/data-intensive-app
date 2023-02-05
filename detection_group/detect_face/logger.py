import logging

from config import settings


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(settings.LOG_PATH, mode="w")
formatter    = logging.Formatter('%(asctime)s:%(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
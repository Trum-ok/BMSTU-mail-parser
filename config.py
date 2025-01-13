import os
from dotenv import load_dotenv

load_dotenv(override=True, encoding='utf-8')

TG_TOKEN = os.getenv('TG_TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

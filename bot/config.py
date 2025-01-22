import os
from typing import List
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    PORT:int
    HOST:str
    BASE_URL: str
    ADMIN_IDS: List[int]
    FORMAT_LOG: str = (
        "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )
    LOG_ROTATION: str = "10 MB"
    DB_URL: str = 'sqlite+aiosqlite:///data/db.sqlite3'

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )
    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

# Получаем параметры для загрузки переменных среды
settings = Settings()

# Инициализируем бота и диспетчер
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
admins = settings.ADMIN_IDS
PORT = settings.PORT
HOST = settings.HOST
BASE_URL = settings.BASE_URL
WEBHOOK_PATH = '/webhook'

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.log")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
DATABASE_LITE_URL = settings.DB_URL
DATABASE_PG_URL = "postgresql+asyncpg://postgres_container:postgres_container@172.18.0.2:5432/postgres"
# DATABASE_PG_URL = settings.get_db_url()

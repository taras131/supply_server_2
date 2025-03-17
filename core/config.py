from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True
    BOT_TOKEN: str = "7588156307:AAH3JN6qVxxjyJ3y1lMeYmekGvG5P-eEFnQ"
    WEBHOOK_URL: str = "https://mylittleserver.ru/api/v1/bot/webhook"


settings = Settings()

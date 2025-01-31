from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from core.models import Base, db_helper
from api_v1 import router as api_v1_router
from core.config import settings
from bot.bot import start_bot
import asyncio
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram import Update


async def error_handler(update: Update, context: CallbackContext):
    # Логируем исключение
    print("Произошла ошибка:", context.error)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    asyncio.create_task(start_bot())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

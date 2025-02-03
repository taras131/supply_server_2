import uvicorn
from core.models import Base, db_helper
from api_v1 import router as api_v1_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from api_v1.bot.bot import handle_message, set_webhook
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    webhook_info = await set_webhook()
    print("Webhook setup response:", webhook_info)
    yield

    # Остановка бота при завершении работы сервера
    print("Shutting down")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретные домены вместо "*"
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

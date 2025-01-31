from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Subscriber  # Модель подписчика
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.engine import Result
from telegram.error import Forbidden


async def get_subscribers(session: AsyncSession) -> list[Subscriber]:
    stmt = select(Subscriber).order_by(Subscriber.id)
    try:
        result: Result = await session.execute(stmt)
        subscribers = result.scalars().unique().all()  # Получаем уникальные записи
        return list(subscribers)
    except Exception as e:
        print(f"Error fetching subscribers: {e}")  # Логируем ошибку
        raise HTTPException(status_code=500, detail="Ошибка при получении подписчиков")

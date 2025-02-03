from core.models import Subscriber
from api_v1.bot.bot import SubscriberCreateSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from fastapi import HTTPException


async def create_subscriber(
    session: AsyncSession,
    subscriber_in: SubscriberCreateSchema,
) -> Subscriber:
    subscriber = Subscriber(
        chat_id=subscriber_in.chat_id,
        username=subscriber_in.username,
        is_active=subscriber_in.is_active,
    )
    session.add(subscriber)
    await session.commit()
    await session.refresh(subscriber)
    return subscriber


async def get_subscriber_by_chat_id(
    session: AsyncSession,
    chat_id: int,
) -> Subscriber | None:
    stmt = select(Subscriber).where(Subscriber.chat_id == chat_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_subscribers(session: AsyncSession) -> list[Subscriber]:
    stmt = select(Subscriber).order_by(Subscriber.id)
    try:
        result: Result = await session.execute(stmt)
        subscribers = result.scalars().unique().all()  # Получаем уникальные записи
        return list(subscribers)
    except Exception as e:
        print(f"Error fetching subscribers: {e}")  # Логируем ошибку
        raise HTTPException(status_code=500, detail="Ошибка при получении подписчиков")

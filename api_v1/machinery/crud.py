from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from core.models import Machinery
from .schemas import MachineryCreate, MachineryUpdate


async def get_machinery(session: AsyncSession) -> list[Machinery]:
    stmt = select(Machinery).order_by(Machinery.id)
    result: Result = await session.execute(stmt)
    machinery = result.scalars().all()
    return list(machinery)


async def get_machinery_by_id(
    session: AsyncSession,
    machinery_id: int,
) -> Machinery | None:
    return await session.get(Machinery, machinery_id)


async def create_machinery(
    session: AsyncSession,
    machinery_in: MachineryCreate,
) -> Machinery:
    machinery = Machinery(**machinery_in.model_dump())
    session.add(machinery)
    await session.commit()
    await session.refresh(machinery)
    return machinery


async def update_machinery(
    session: AsyncSession,
    machinery: Machinery,
    machinery_update: MachineryUpdate,
) -> Machinery:
    for name, value in machinery_update.model_dump().items():
        setattr(machinery, name, value)
    await session.commit()
    await session.refresh(machinery)
    return machinery


async def delete_machinery(
    session: AsyncSession,
    machinery: Machinery,
) -> None:
    await session.delete(machinery)
    await session.commit()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from .schemas import ShipmentsCreateSchema, ShipmentsSchema, ShipmentsUpdateSchema
from core.models import Shipments


async def get_all(
    session: AsyncSession,
) -> list[Shipments]:
    stmt = select(Shipments).execution_options(fresh=True)
    try:
        result = await session.execute(stmt)
        shipments_list = result.scalars().all()
        return shipments_list
    except Exception as e:
        print(f"Error fetching shipments: {str(e)}")
        raise


async def create(
    session: AsyncSession,
    shipment_in: ShipmentsCreateSchema,
) -> Shipments:
    try:
        shipment = Shipments(**shipment_in.model_dump())
        session.add(shipment)
        await session.commit()
        await session.refresh(shipment)
        return shipment
    except Exception as e:
        print(f"Error creating shipment: {e}")
        raise e


async def get_by_id(
    session: AsyncSession,
    shipment_id: int,
) -> Shipments | None:
    stmt = select(Shipments).where(Shipments.id == shipment_id)
    try:
        result = await session.execute(stmt)
        shipment = result.scalar_one_or_none()
        if shipment is None:
            return None
        return shipment
    except Exception as e:
        print(f"Error fetching shipment: {str(e)}")
        raise


async def update(
    session: AsyncSession,
    shipment: Shipments,
    shipment_update: ShipmentsUpdateSchema,
) -> Shipments:
    for name, value in shipment_update.model_dump().items():
        setattr(shipment, name, value)
    await session.commit()
    await session.refresh(shipment)
    return shipment


async def delete(
    session: AsyncSession,
    shipment: Shipments,
) -> None:
    await session.delete(shipment)
    await session.commit()

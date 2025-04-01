from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import (
    db_helper,
    Shipments,
)
from . import crud


async def shipment_by_id(
    shipment_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Shipments:
    shipment = await crud.get_by_id(session=session, shipment_id=shipment_id)
    if shipment is not None:
        return shipment
    raise HTTPException(status_code=404, detail="shipment not found")

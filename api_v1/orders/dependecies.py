from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import (
    db_helper,
    Orders,
)
from . import crud


async def order_by_id(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Orders:
    order = await crud.get_by_id(session=session, order_id=order_id)
    if order is not None:
        return order
    raise HTTPException(status_code=404, detail="order not found")

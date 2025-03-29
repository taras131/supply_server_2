from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import (
    db_helper,
    Suppliers,
)
from . import crud


async def supplier_by_id(
    supplier_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Suppliers:
    supplier = await crud.get_supplier_by_id(session=session, supplier_id=supplier_id)
    if supplier is not None:
        return supplier
    raise HTTPException(status_code=404, detail="supplier not found")

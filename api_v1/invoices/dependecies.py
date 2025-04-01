from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import (
    db_helper,
    Invoices,
)
from . import crud


async def invoice_by_id(
    invoice_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Invoices:
    invoice = await crud.get_by_id(session=session, invoice_id=invoice_id)
    if invoice is not None:
        return invoice
    raise HTTPException(status_code=404, detail="invoice not found")

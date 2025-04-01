from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import InvoicesCreateSchema, InvoicesSchema, InvoicesUpdateSchema
from .dependecies import invoice_by_id
from . import crud
from core.models import (
    db_helper,
    Invoices,
)

router = APIRouter(tags=["Invoices"])


@router.get("/", response_model=List[InvoicesSchema])
async def get_invoices(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all(session=session)


@router.get("/{invoice_id}/", response_model=InvoicesSchema)
async def get_invoice_by_id(
    invoice_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    invoice = await crud.get_by_id(session, invoice_id)
    if invoice is None:
        raise HTTPException(
            status_code=404, detail=f"Invoice with id {invoice_id} not found"
        )
    return invoice


@router.post("/", response_model=InvoicesSchema)
async def create_invoice(
    invoice_in: InvoicesCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    invoice = await crud.create(session=session, invoice_in=invoice_in)
    return invoice


@router.put("/{invoice_id}/", response_model=InvoicesSchema)
async def update_invoice(
    invoice_update: InvoicesUpdateSchema,
    invoice: Invoices = Depends(invoice_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update(
        session=session,
        invoice=invoice,
        invoice_update=invoice_update,
    )


@router.delete("/{invoice_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice_by_id(
    invoice: Invoices = Depends(invoice_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete(session=session, invoice=invoice)

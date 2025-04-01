from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import SupplierSchema, SupplierCreateSchema, SupplierUpdateSchema
from .dependecies import supplier_by_id
from . import crud
from core.models import (
    db_helper,
    Suppliers,
)

router = APIRouter(tags=["Suppliers"])


@router.get("/", response_model=List[SupplierSchema])
async def get_suppliers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all(session=session)


@router.get("/{supplier_id}/", response_model=SupplierSchema)
async def get_supplier_by_id(
    supplier_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    supplier = await crud.get_supplier_by_id(session, supplier_id)
    if supplier is None:
        raise HTTPException(
            status_code=404, detail=f"Supplier with id {supplier_id} not found"
        )
    return supplier


@router.post("/", response_model=SupplierSchema)
async def create_supplier(
    supplier_in: SupplierCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    supplier = await crud.create_supplier(session=session, supplier_in=supplier_in)
    return supplier


@router.put("/{supplier_id}/", response_model=SupplierSchema)
async def update_supplier(
    supplier_update: SupplierUpdateSchema,
    supplier: Suppliers = Depends(supplier_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_supplier(
        session=session,
        supplier=supplier,
        supplier_update=supplier_update,
    )


@router.delete("/{supplier_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier_by_id(
    supplier: Suppliers = Depends(supplier_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_supplier(session=session, supplier=supplier)

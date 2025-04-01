from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ShipmentsSchema, ShipmentsCreateSchema, ShipmentsUpdateSchema
from .dependecies import shipment_by_id
from . import crud
from core.models import (
    db_helper,
    Shipments,
)

router = APIRouter(tags=["Shipments"])


@router.get("/", response_model=List[ShipmentsSchema])
async def get_shipments(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all(session=session)


@router.get("/{shipment_id}/", response_model=ShipmentsSchema)
async def get_shipment_by_id(
    shipment_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    shipment = await crud.get_by_id(session, shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=404, detail=f"Shipment with id {shipment_id} not found"
        )
    return shipment


@router.post("/", response_model=ShipmentsSchema)
async def create_shipment(
    shipment_in: ShipmentsCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    shipment = await crud.create(session=session, shipment_in=shipment_in)
    return shipment


@router.put("/{shipment_id}/", response_model=ShipmentsSchema)
async def update_shipment(
    shipment_update: ShipmentsUpdateSchema,
    shipment: Shipments = Depends(shipment_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update(
        session=session,
        shipment=shipment,
        shipment_update=shipment_update,
    )


@router.delete("/{shipment_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment_by_id(
    shipment: Shipments = Depends(shipment_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete(session=session, shipment=shipment)

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import OrdersCreateSchema, OrdersSchema, OrdersUpdateSchema
from .dependecies import order_by_id
from . import crud
from core.models import (
    db_helper,
    Shipments,
    Orders,
)


router = APIRouter(tags=["Orders"])


@router.get("/", response_model=List[OrdersSchema])
async def get_orders(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all(session=session)


@router.get("/{order_id}/", response_model=OrdersSchema)
async def get_order_by_id(
    order_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    order = await crud.get_by_id(session, order_id)
    if order is None:
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found"
        )
    return order


@router.post("/", response_model=OrdersSchema)
async def create_shipment(
    order_in: OrdersCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    shipment = await crud.create(session=session, order_in=order_in)
    return shipment


@router.put("/{shipment_id}/", response_model=OrdersSchema)
async def update_shipment(
    order_update: OrdersUpdateSchema,
    order: Orders = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update(
        session=session,
        order=order,
        order_update=order_update,
    )


@router.delete("/{order_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_by_id(
    order: Orders = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete(session=session, order=order)

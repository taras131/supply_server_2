from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from .dependecies import machinery_by_id
from . import crud
from .schemas import Machinery, MachineryCreate, MachineryUpdate

router = APIRouter(tags=["Machinery"])


@router.get("/", response_model=list[Machinery])
async def get_machinery(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_machinery(session=session)


@router.post("/", response_model=Machinery)
async def create_machinery(
    machinery_in: MachineryCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_machinery(
        session=session,
        machinery_in=machinery_in,
    )


@router.get("/{machinery_id}/", response_model=Machinery)
async def get_machinery_by_id(
    machinery: Machinery = Depends(machinery_by_id),
):
    return machinery


@router.put("/{machinery_id}/", response_model=Machinery)
async def update_machinery(
    machinery_update: MachineryUpdate,
    machinery: Machinery = Depends(machinery_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_machinery(
        session=session,
        machinery=machinery,
        machinery_update=machinery_update,
    )


@router.delete("/{machinery_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_machinery_by_id(
    machinery: Machinery = Depends(machinery_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_machinery(session=session, machinery=machinery)

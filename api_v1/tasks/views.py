from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, MachineryTask
from .dependecies import task_by_id
from . import crud
from .schemas import (
    TaskCreateSchema,
    TaskSchema,
    TaskUpdateSchema,
)

router = APIRouter(tags=["Tasks"])

# router.include_router(ws_router)


@router.get("/", response_model=List[TaskSchema])
async def get_tasks(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all(session=session)


@router.post("/", response_model=TaskSchema)
async def create_task(
    task_in: TaskCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_task(session=session, task_in=task_in)


@router.put("/{task_id}/", response_model=TaskSchema)
async def update_task(
    task_update: TaskUpdateSchema,
    task: MachineryTask = Depends(task_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_task(
        session=session,
        task=task,
        task_update=task_update,
    )


@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(
    task: MachineryTask = Depends(task_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_task(session=session, task=task)

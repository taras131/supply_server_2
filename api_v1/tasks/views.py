from fastapi import APIRouter, HTTPException, Depends, status, WebSocket
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Machinery, MachineryComment
from . import crud
from .schemas import (
    TaskCreateSchema,
    TaskSchema,
)

router = APIRouter(tags=["Tasks"])


@router.post("/", response_model=TaskSchema)
async def create_machinery(
    task_in: TaskCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    task = await crud.create_task(session=session, task_in=task_in)
    return JSONResponse(
        content=task.to_dict(), headers={"Access-Control-Allow-Origin": "*"}
    )

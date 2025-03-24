from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import (
    db_helper,
    MachineryTask,
)
from . import crud


async def task_by_id(
    task_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> MachineryTask:
    task = await crud.get_task_by_id(session=session, task_id=task_id)
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

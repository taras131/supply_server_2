from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import db_helper, Machinery, MachineryComment, MachineryTask
from . import crud


async def machinery_by_id(
    machinery_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Machinery:
    machinery = await crud.get_machinery_by_id(
        session=session, machinery_id=machinery_id
    )
    if machinery is not None:
        return machinery
    raise HTTPException(status_code=404, detail="Machinery not found")


async def comment_by_id(
    comment_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> MachineryComment:
    comment = await crud.get_comment_by_id(session=session, comment_id=comment_id)
    if comment is not None:
        return comment
    raise HTTPException(status_code=404, detail="Machinery not found")


async def task_by_id(
    task_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> MachineryTask:
    task = await crud.get_task_by_id(session=session, task_id=task_id)
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

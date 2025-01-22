from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from core.models import Machinery, MachineryComment, MachineryDocs, Task
from fastapi import APIRouter, UploadFile, File, HTTPException
from .schemas import (
    TaskCreateSchema,
    TaskSchema,
)


async def create_task(
    session: AsyncSession,
    task_in: TaskCreateSchema,
) -> Task:
    try:
        task = Task(**task_in.model_dump())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
    except Exception as e:
        print(f"Error creating task: {e}")
        raise e

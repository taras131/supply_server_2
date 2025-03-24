from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from core.models import (
    Machinery,
    MachineryComment,
    MachineryDocs,
    MachineryTask,
    MachineryProblem,
    Subscriber,
)
from fastapi import HTTPException
import logging
from .schemas import (
    TaskCreateSchema,
    TaskUpdateSchema,
)


async def get_all(
    session: AsyncSession,
) -> list[MachineryTask]:
    stmt = select(MachineryTask).execution_options(fresh=True)
    try:
        result = await session.execute(stmt)
        tasks_list = result.scalars().all()
        return tasks_list
    except Exception as e:
        print(f"Error fetching machinery: {str(e)}")
        raise


async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> MachineryTask | None:
    stmt = select(MachineryTask).where(MachineryTask.id == task_id)
    try:
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()
        if task is None:
            return None
        return task
    except Exception as e:
        print(f"Error fetching machinery: {str(e)}")
        raise


async def create_task(
    session: AsyncSession,
    task_in: TaskCreateSchema,
) -> MachineryTask:
    try:
        task = MachineryTask(**task_in.model_dump())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
    except Exception as e:
        print(f"Error creating task: {e}")
        raise e


async def update_task(
    session: AsyncSession,
    task: MachineryTask,
    task_update: TaskUpdateSchema,
) -> MachineryTask:
    for name, value in task_update.model_dump().items():
        setattr(task, name, value)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(
    session: AsyncSession,
    task: MachineryTask,
) -> None:
    await session.delete(task)
    await session.commit()

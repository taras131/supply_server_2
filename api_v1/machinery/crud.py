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
    MachinerySchema,
    MachineryCommentSchema,
    MachineryCreateSchema,
    MachineryUpdateSchema,
    MachineryCommentCreateSchema,
    MachineryCommentUpdateSchema,
    DocsCreateSchema,
    MachineryCompleteSchema,
    TaskCreateSchema,
    TaskUpdateSchema,
    ProblemCreateSchema,
)


async def get_machinery(session: AsyncSession) -> list[Machinery]:
    stmt = (
        select(Machinery)
        .options(
            selectinload(Machinery.comments.and_(MachineryComment.is_active == True))
        )
        .order_by(Machinery.id)
    )
    try:
        result: Result = await session.execute(stmt)
        machinery = result.scalars().unique().all()  # Добавляем unique()
        return list(machinery)
    except Exception as e:
        print(f"Error fetching machinery: {e}")
        raise


async def get_machinery_list(session: AsyncSession):
    stmt = select(Machinery).execution_options(fresh=True)
    await session.flush()
    result = await session.execute(stmt)
    machinery_list = result.scalars().all()
    return machinery_list


async def get_machinery_by_id(
    session: AsyncSession,
    machinery_id: int,
) -> Machinery | None:
    stmt = (
        select(Machinery)
        .where(Machinery.id == machinery_id)
        .options(
            selectinload(Machinery.comments),
            selectinload(Machinery.docs),
            selectinload(Machinery.tasks),
            selectinload(Machinery.problems),
        )
    )
    try:
        result = await session.execute(stmt)
        machinery = result.scalar_one_or_none()
        if machinery is None:
            return None
        return machinery
    except Exception as e:
        print(f"Error fetching machinery: {str(e)}")
        raise


async def get_comment_by_id(
    session: AsyncSession,
    comment_id: int,
) -> MachineryComment | None:
    return await session.get(MachineryComment, comment_id)


async def create_machinery(
    session: AsyncSession,
    machinery_in: MachineryCreateSchema,
) -> Machinery:
    machinery = Machinery(**machinery_in.model_dump())
    session.add(machinery)
    await session.commit()
    await session.refresh(machinery)
    return machinery


async def update_machinery(
    session: AsyncSession,
    machinery: Machinery,
    machinery_update: MachineryCompleteSchema,
) -> Machinery | None:
    # Обновляем основные поля
    for name, value in machinery_update.model_dump().items():
        if (
            name != "comments"
            and name != "docs"
            and name != "tasks"
            and name != "problems"
        ):
            setattr(machinery, name, value)

    # Сохраняем изменения
    await session.commit()

    # Загружаем связанные данные после обновления
    stmt = (
        select(Machinery)
        .where(Machinery.id == machinery.id)
        .options(
            selectinload(Machinery.comments),  # Загружаем комментарии
            selectinload(Machinery.docs),  # Загружаем документы
            selectinload(Machinery.tasks),  # Загружаем задачи
            # Если есть другие связанные таблицы, добавьте их здесь
        )
    )
    result = await session.execute(stmt)
    machinery = result.scalar_one_or_none()
    if machinery is None:
        return None

    return machinery


async def delete_machinery(
    session: AsyncSession,
    machinery: Machinery,
) -> None:
    await session.delete(machinery)
    await session.commit()


async def create_comment(
    session: AsyncSession,
    comment_in: MachineryCommentCreateSchema,
) -> MachineryComment:
    print(comment_in)
    comment = MachineryComment(**comment_in.model_dump())
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def delete_comment(
    session: AsyncSession,
    comment: MachineryCommentSchema,
) -> None:
    await session.delete(comment)
    await session.commit()


async def update_machinery_comment(
    session: AsyncSession,
    comment: MachineryComment,
    comment_update: MachineryCommentUpdateSchema,
) -> MachineryComment:
    for name, value in comment_update.model_dump().items():
        setattr(comment, name, value)
    await session.commit()
    await session.refresh(comment)
    return comment


async def create_doc(
    session: AsyncSession,
    doc_in: DocsCreateSchema,
) -> MachineryDocs:
    print(doc_in)
    doc = MachineryDocs(**doc_in.model_dump())
    session.add(doc)
    await session.commit()
    await session.refresh(doc)
    return doc


async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> MachineryTask | None:
    # Создаем запрос с предварительной загрузкой всех связанных данных
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


async def create_problem(
    session: AsyncSession,
    problem_in: ProblemCreateSchema,
) -> MachineryProblem:
    try:
        problem = MachineryProblem(**problem_in.model_dump())
        session.add(problem)
        await session.commit()
        await session.refresh(problem)
        return problem
    except Exception as e:
        print(f"Error creating problem: {e}")
        raise e

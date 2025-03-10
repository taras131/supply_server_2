from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import (
    db_helper,
    Machinery,
    MachineryComment,
    MachineryTask,
    MachineryProblem,
)
from .dependecies import machinery_by_id, comment_by_id, task_by_id, problem_by_id
from .machinery_ws import router as ws_router
from api_v1.bot.crud import get_subscribers
from api_v1.bot.bot import send_telegram_message
from . import crud
from .schemas import (
    MachinerySchema,
    MachineryCommentSchema,
    MachineryCreateSchema,
    MachineryCompleteSchema,
    MachineryUpdateSchema,
    MachineryCommentCreateSchema,
    MachineryCommentUpdateSchema,
    DocsCreateSchema,
    TaskCreateSchema,
    TaskSchema,
    TaskUpdateSchema,
    ProblemSchema,
    ProblemCreateSchema,
)

router = APIRouter(tags=["Machinery"])

router.include_router(ws_router)


@router.post("/", response_model=MachinerySchema)
async def create_machinery(
    machinery_in: MachineryCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_machinery(
        session=session,
        machinery_in=machinery_in,
    )


@router.get("/{machinery_id}/", response_model=MachineryCompleteSchema)
async def get_machinery_by_id(
    machinery_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    machinery = await crud.get_machinery_by_id(session, machinery_id)
    if machinery is None:
        raise HTTPException(
            status_code=404, detail=f"Machinery with id {machinery_id} not found"
        )
    return machinery


@router.put("/{machinery_id}/", response_model=MachineryCompleteSchema)
async def update_machinery(
    machinery_update: MachineryUpdateSchema,
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


@router.post("/comment/")
async def create_comment(
    comment_in: MachineryCommentCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_comment(session=session, comment_in=comment_in)


@router.delete("/comment/{comment_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_by_id(
    comment: MachineryCommentSchema = Depends(comment_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_comment(session=session, comment=comment)


@router.put("/comment/{comment_id}/", response_model=MachineryCommentSchema)
async def update_machinery_comment(
    comment_update: MachineryCommentUpdateSchema,
    comment: MachineryComment = Depends(comment_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_machinery_comment(
        session=session,
        comment=comment,
        comment_update=comment_update,
    )


@router.post("/docs/")
async def create_doc(
    doc_in: DocsCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    print("Новый документ")
    print(doc_in)
    return await crud.create_doc(session=session, doc_in=doc_in)


@router.post("/tasks/", response_model=TaskSchema)
async def create_task(
    task_in: TaskCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    return await crud.create_task(session=session, task_in=task_in)


@router.put("/tasks/{task_id}/", response_model=TaskSchema)
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


@router.post("/problems/", response_model=ProblemSchema)
async def create_problem(
    problem_in: ProblemCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    problem = await crud.create_problem(session=session, problem_in=problem_in)
    subscribers = await get_subscribers(session)
    machinery = await crud.get_machinery_by_id(
        session=session, machinery_id=problem.machinery_id
    )
    message_text = (
        f"🔔 Новая проблема:\n"
        f"Техника: {machinery.brand} {machinery.model}\n"
        f"Гос номер: {machinery.state_number}\n"
        f"Название: {problem.title}\n"
        f"Описание: {problem.description}\n"
        f"Приоритет: {problem.priority_id}\n"
        f"ID техники: {problem.machinery_id}"
    )
    # Отправляем сообщение каждому активному подписчику
    for subscriber in subscribers:
        if subscriber.is_active:
            try:
                await send_telegram_message(
                    chat_id=subscriber.chat_id, text=message_text
                )
            except Exception as e:
                print(f"Failed to send message to {subscriber.chat_id}: {str(e)}")
                continue
    return problem


@router.put("/problems/{problem_id}/", response_model=ProblemSchema)
async def update_machinery_comment(
    problem_update: ProblemSchema,
    problem: MachineryProblem = Depends(problem_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_machinery_problem(
        session=session,
        problem=problem,
        problem_update=problem_update,
    )

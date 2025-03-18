from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .problems_ws import router as ws_router
from .schemas import ProblemSchema, ProblemCreateSchema
from api_v1.bot.crud import get_subscribers
from api_v1.bot.bot import send_telegram_message
from api_v1.machinery.crud import get_machinery_by_id
from .dependecies import problem_by_id
from . import crud
from core.models import (
    db_helper,
    Machinery,
    MachineryComment,
    MachineryTask,
    MachineryProblem,
)

router = APIRouter(tags=["Problems"])

router.include_router(ws_router)


@router.post("/", response_model=ProblemSchema)
async def create_problem(
    problem_in: ProblemCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    problem = await crud.create_problem(session=session, problem_in=problem_in)
    subscribers = await get_subscribers(session)
    machinery = await get_machinery_by_id(
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


@router.put("/{problem_id}/", response_model=ProblemSchema)
async def update_machinery_problem(
    problem_update: ProblemSchema,
    problem: MachineryProblem = Depends(problem_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_machinery_problem(
        session=session,
        problem=problem,
        problem_update=problem_update,
    )


@router.delete("/{problem_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_problem_by_id(
    problem: MachineryProblem = Depends(problem_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_problem(session=session, problem=problem)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from .schemas import ProblemCreateSchema, ProblemSchema
from core.models import (
    Machinery,
    MachineryComment,
    MachineryDocs,
    MachineryTask,
    MachineryProblem,
    Subscriber,
)


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


async def get_problems_list(session: AsyncSession):
    stmt = select(MachineryProblem).execution_options(fresh=True)
    await session.flush()
    result = await session.execute(stmt)
    problems_list = result.scalars().all()
    return problems_list


async def get_problem_by_id(
    session: AsyncSession,
    problem_id: int,
) -> MachineryProblem | None:
    stmt = select(MachineryProblem).where(MachineryProblem.id == problem_id)
    try:
        result = await session.execute(stmt)
        problem = result.scalar_one_or_none()
        if problem is None:
            return None
        return problem
    except Exception as e:
        print(f"Error fetching machinery: {str(e)}")
        raise


async def update_machinery_problem(
    session: AsyncSession,
    problem: MachineryProblem,
    problem_update: ProblemSchema,
) -> MachineryProblem:
    for name, value in problem_update.model_dump().items():
        setattr(problem, name, value)
    await session.commit()
    await session.refresh(problem)
    return problem


async def delete_problem(
    session: AsyncSession,
    problem: MachineryProblem,
) -> None:
    await session.delete(problem)
    await session.commit()

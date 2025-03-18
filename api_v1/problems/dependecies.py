from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import (
    db_helper,
    Machinery,
    MachineryComment,
    MachineryTask,
    MachineryProblem,
)
from . import crud


async def problem_by_id(
    problem_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> MachineryProblem:
    problem = await crud.get_problem_by_id(session=session, problem_id=problem_id)
    if problem is not None:
        return problem
    raise HTTPException(status_code=404, detail="problem not found")

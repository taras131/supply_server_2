from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import db_helper, Machinery
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

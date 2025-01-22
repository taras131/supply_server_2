from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User
from .schemas import UserCreateSchema
from core.security import get_password_hash, verify_password


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    user_in: UserCreateSchema,
) -> User:
    user = User(
        email=user_in.email,
        password=get_password_hash(user_in.password),
        first_name=user_in.first_name,
        middle_name=user_in.middle_name,
        role_id=user_in.role_id,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> User | None:
    user = await get_user_by_email(session, email)
    if not user or not verify_password(password, user.password):
        return None
    return user


async def get_users_list(session: AsyncSession):
    stmt = select(User).execution_options(fresh=True)
    await session.flush()
    result = await session.execute(stmt)
    users_list = result.scalars().all()
    return users_list

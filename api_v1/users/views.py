from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User
from . import crud
from .schemas import UserCreateSchema, UserResponseSchema, TokenSchema, UserAuthSchema
from .users_ws import router as ws_router
from .dependecies import get_current_user, generate_access_token


router = APIRouter(tags=["Auth"])


router.include_router(ws_router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=UserResponseSchema)
async def register(
    user_in: UserCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    existing_user = await crud.get_user_by_email(session, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    return await crud.create_user(session=session, user_in=user_in)


@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: UserAuthSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.authenticate_user(
        session=session, email=form_data.email, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = generate_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/check", response_model=TokenSchema)
async def check_auth_and_refresh_token(
    current_user: User = Depends(get_current_user),  # Проверяем токен
):
    access_token = generate_access_token(current_user)
    return {"access_token": access_token, "token_type": "bearer"}

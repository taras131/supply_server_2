from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from core.models import db_helper
from core.security import SECRET_KEY, ALGORITHM
from . import crud
from datetime import timedelta
from core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from core.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(token)
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_email(session=session, email=email)
    if user is None:
        raise credentials_exception

    return user


def generate_access_token(user: User) -> str:
    """
    Генерация JWT токена на основе модели пользователя.
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "email": user.email,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "role_id": user.role_id,
            "id": user.id,
        },
        expires_delta=access_token_expires,
    )
    return access_token

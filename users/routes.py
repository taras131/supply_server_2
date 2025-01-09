from fastapi import APIRouter
from users.shemas import CreateUser
from users import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_user(user: CreateUser):
    return crud.create_user(user)


@router.get("/")
async def get_all():
    return {"users:": "users"}

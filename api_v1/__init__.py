from fastapi import APIRouter
from .machinery.views import router as machinery_router
from .users.views import router as users_router
from .files.views import router as files_router
from .bot.views import router as bot_router

router = APIRouter()
router.include_router(machinery_router, prefix="/machinery")
router.include_router(users_router, prefix="/auth")
router.include_router(files_router, prefix="/files")
router.include_router(bot_router, prefix="/bot")

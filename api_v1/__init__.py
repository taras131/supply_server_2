from fastapi import APIRouter
from .machinery.views import router as machinery_router
from .problems.views import router as problems_router
from .tasks.views import router as tasks_router
from .users.views import router as users_router
from .suppliers.views import router as suppliers_router
from .files.views import router as files_router
from .bot.views import router as bot_router

router = APIRouter()
router.include_router(machinery_router, prefix="/machinery")
router.include_router(problems_router, prefix="/problems")
router.include_router(tasks_router, prefix="/tasks")
router.include_router(users_router, prefix="/auth")
router.include_router(suppliers_router, prefix="/suppliers")
router.include_router(files_router, prefix="/files")
router.include_router(bot_router, prefix="/bot")

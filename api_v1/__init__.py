from fastapi import APIRouter
from .machinery.views import router as machinery_router
from .files.views import router as files_router

router = APIRouter()
router.include_router(machinery_router, prefix="/machinery")
router.include_router(files_router, prefix="/files")

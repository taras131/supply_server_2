from fastapi import APIRouter
from .machinery.views import router as machinery_router

router = APIRouter()
router.include_router(machinery_router, prefix="/machinery")

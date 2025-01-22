from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from api_v1 import router as api_v1_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from api_v1.users.views import router as auth_router
from api_v1.tasks.views import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В реальном приложении укажите конкретные разрешённые домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(tasks_router, prefix="/api/v1/tasks")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

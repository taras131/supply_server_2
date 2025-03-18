from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import asyncio, time
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import event
from core.models import db_helper, MachineryProblem
from core.websocket_utils import State, get_data_hash
from .crud import get_problems_list
import hashlib

state = State()


@event.listens_for(MachineryProblem, "after_update")
def receive_machinery_after_update(mapper, connection, target):
    asyncio.create_task(state.notify_changed())


@event.listens_for(MachineryProblem, "after_insert")
def receive_machinery_after_insert(mapper, connection, target):
    asyncio.create_task(state.notify_changed())


@event.listens_for(MachineryProblem, "after_delete")
def receive_machinery_after_delete(mapper, connection, target):
    asyncio.create_task(state.notify_changed())


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        await websocket.accept()
        print("WebSocket соединение установлено")
        problems_list = await get_problems_list(session)
        state.last_data = [problem.to_dict() for problem in problems_list]
        await websocket.send_json(state.last_data)

        while True:
            try:
                await asyncio.wait_for(state.changed_queue.get(), timeout=50)
                await asyncio.sleep(0.5)

                session.expire_all()
                problems_list = await get_problems_list(session)
                current_data = [problem.to_dict() for problem in problems_list]

                if get_data_hash(current_data) != get_data_hash(state.last_data):
                    state.last_data = current_data
                    await websocket.send_json(current_data)

            except Exception as e:
                print(f"Ошибка при обработке: {str(e)}")
                await websocket.close()
                break

    except WebSocketDisconnect:
        print("WebSocket соединение закрыто клиентом")

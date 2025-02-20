from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_users_list
from core.websocket_utils import State, get_data_hash
from core.models import db_helper, User
import asyncio

state = State()


@event.listens_for(User, "after_update")
def receive_after_update(mapper, connection, target):
    asyncio.run_coroutine_threadsafe(state.notify_changed(), asyncio.get_event_loop())


@event.listens_for(User, "after_insert")
def receive_after_insert(mapper, connection, target):
    asyncio.run_coroutine_threadsafe(state.notify_changed(), asyncio.get_event_loop())


@event.listens_for(User, "after_delete")
def receive_after_delete(mapper, connection, target):
    asyncio.run_coroutine_threadsafe(state.notify_changed(), asyncio.get_event_loop())


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        await websocket.accept()
        users_list = await get_users_list(session)
        state.last_data = [users.to_dict() for users in users_list]
        await websocket.send_json(state.last_data)
        while True:
            # Ожидаем уведомления об изменениях
            await state.changed_queue.get()

            # Получаем обновленные данные
            session.expire_all()
            users_list = await get_users_list(session)
            current_data = [user.to_dict() for user in users_list]
            current_hash = get_data_hash(current_data)
            last_hash = get_data_hash(state.last_data)
            if current_hash != last_hash:
                state.last_data = current_data
                await websocket.send_json(current_data)
    except WebSocketDisconnect:
        print("Клиент отключился")
    except Exception as e:
        print(f"WebSocket ошибка: {e}")

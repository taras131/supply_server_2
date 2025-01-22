from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import event
from core.models import db_helper, Machinery, MachineryComment
from core.websocket_utils import State, get_data_hash
from .crud import get_machinery_list
import hashlib


state = State()


@event.listens_for(MachineryComment, "after_update")
def receive_comment_after_update(mapper, connection, target):
    state.changed = True


@event.listens_for(MachineryComment, "after_insert")
def receive_comment_after_insert(mapper, connection, target):
    state.changed = True


@event.listens_for(MachineryComment, "after_delete")
def receive_comment_after_delete(mapper, connection, target):
    state.changed = True


# Регистрируем слушателей событий SQLAlchemy
@event.listens_for(Machinery, "after_update")
def receive_after_update(mapper, connection, target):
    state.changed = True


@event.listens_for(Machinery, "after_insert")
def receive_after_insert(mapper, connection, target):
    state.changed = True


@event.listens_for(Machinery, "after_delete")
def receive_after_delete(mapper, connection, target):
    state.changed = True


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        await websocket.accept()

        # Получаем начальные данные
        machinery_list = await get_machinery_list(session)
        state.last_data = [machinery.to_dict() for machinery in machinery_list]
        await websocket.send_json(state.last_data)

        while True:
            if state.changed:
                session.expire_all()
                machinery_list = await get_machinery_list(session)
                current_data = [machinery.to_dict() for machinery in machinery_list]
                current_hash = get_data_hash(current_data)
                last_hash = get_data_hash(state.last_data)
                if current_hash != last_hash:
                    state.last_data = current_data
                    await websocket.send_json(current_data)
                state.changed = False

            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("Клиент отключился")
    except Exception as e:
        print(f"WebSocket ошибка: {e}")
    """
    finally:
        await websocket.close()
    """

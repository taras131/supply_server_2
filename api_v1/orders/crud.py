from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from .schemas import OrdersCreateSchema, OrdersUpdateSchema, OrdersSchema
from core.models import (
    Machinery,
    MachineryComment,
    MachineryDocs,
    MachineryTask,
    MachineryProblem,
    Orders,
)


async def create(
    session: AsyncSession,
    order_in: OrdersCreateSchema,
) -> Orders:
    try:
        # Создаем родительский объект заказа
        order_data = order_in.model_dump()
        orders_items_data = order_data.pop("orders_items", [])

        order = Orders(**order_data)
        session.add(order)

        # Создаем строки для `OrdersItems` и связываем с заказом
        for item_data in orders_items_data:
            orders_item = OrdersItems(**item_data)
            orders_item.order = order  # Связываем строку с заказом
            session.add(orders_item)

        await session.commit()
        await session.refresh(order)
        return order
    except Exception as e:
        print(f"Error creating order with items: {e}")
        raise e


async def get_all(session: AsyncSession):
    # Загружаем заказы вместе с их связанными orders_items
    stmt = (
        select(Orders)
        .execution_options(fresh=True)
        .options(selectinload(Orders.orders_items))
    )  # Подгружаем связанные строки через relationship

    await session.flush()
    result = await session.execute(stmt)
    orders_list = result.scalars().all()

    # Вычисляем процент выполнения для каждого заказа
    for order in orders_list:
        if not order.orders_items:
            order.completion_percentage = (
                0  # Если нет связанных строк, процент выполнения равен 0
            )
        else:
            total_items = len(order.orders_items)  # Общее количество элементов
            ordered_items = sum(
                1 for item in order.orders_items if item.is_ordered
            )  # Количество выполненных элементов
            order.completion_percentage = (
                ordered_items / total_items
            ) * 100  # Процент выполнения

    return orders_list


async def get_by_id(
    session: AsyncSession,
    order_id: int,
) -> Orders | None:
    try:
        # Получение заказа с вложенными строками через relationship
        stmt = (
            select(Orders)
            .where(Orders.id == order_id)
            .options(selectinload(Orders.orders_items))  # Подгружаем связанные строки
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"Error fetching order: {str(e)}")
        raise e


async def update(
    session: AsyncSession,
    order: Orders,
    order_update: OrdersUpdateSchema,
) -> Orders:
    try:
        # Обновляем основные данные заказа
        order_data = order_update.model_dump()
        orders_items_data = order_data.pop("orders_items", [])

        for name, value in order_data.items():
            setattr(order, name, value)

        # Обработка вложенных данных `OrdersItems`
        existing_items_ids = {item.id for item in order.orders_items}
        updated_items_ids = {
            item_data.get("id")
            for item_data in orders_items_data
            if item_data.get("id")
        }

        # Удаляем строки, которые больше не присутствуют
        items_to_remove = [
            item for item in order.orders_items if item.id not in updated_items_ids
        ]
        for item in items_to_remove:
            await session.delete(item)

        # Обновляем существующие строки и добавляем новые
        for item_data in orders_items_data:
            if "id" in item_data and item_data["id"] in existing_items_ids:
                # Обновляем существующую строку
                item = next(
                    item for item in order.orders_items if item.id == item_data["id"]
                )
                for name, value in item_data.items():
                    setattr(item, name, value)
            else:
                # Добавляем новую строку
                new_item = OrdersItems(**item_data)
                new_item.order = order
                session.add(new_item)

        await session.commit()
        await session.refresh(order)
        return order
    except Exception as e:
        print(f"Error updating order with items: {e}")
        raise e


async def delete(
    session: AsyncSession,
    order: Orders,
) -> None:
    try:
        # Удаляем строки `OrdersItems`, связанные с заказом
        for item in order.orders_items:
            await session.delete(item)

        # Удаляем сам заказ
        await session.delete(order)
        await session.commit()
    except Exception as e:
        print(f"Error deleting order: {e}")
        raise e

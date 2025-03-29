from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from .schemas import SupplierCreateSchema, SupplierUpdateSchema
from core.models import Suppliers


async def get_all(
    session: AsyncSession,
) -> list[Suppliers]:
    stmt = select(Suppliers).execution_options(fresh=True)
    try:
        result = await session.execute(stmt)
        suppliers_list = result.scalars().all()
        return suppliers_list
    except Exception as e:
        print(f"Error fetching suppliers: {str(e)}")
        raise


async def create_supplier(
    session: AsyncSession,
    supplier_in: SupplierCreateSchema,
) -> Suppliers:
    try:
        supplier = Suppliers(**supplier_in.model_dump())
        session.add(supplier)
        await session.commit()
        await session.refresh(supplier)
        return supplier
    except Exception as e:
        print(f"Error creating supplier: {e}")
        raise e


async def get_supplier_by_id(
    session: AsyncSession,
    supplier_id: int,
) -> Suppliers | None:
    stmt = select(Suppliers).where(Suppliers.id == supplier_id)
    try:
        result = await session.execute(stmt)
        supplier = result.scalar_one_or_none()
        if supplier is None:
            return None
        return supplier
    except Exception as e:
        print(f"Error fetching machinery: {str(e)}")
        raise


async def update_supplier(
    session: AsyncSession,
    supplier: Suppliers,
    supplier_update: SupplierUpdateSchema,
) -> Suppliers:
    for name, value in supplier_update.model_dump().items():
        setattr(supplier, name, value)
    await session.commit()
    await session.refresh(supplier)
    return supplier


async def delete_supplier(
    session: AsyncSession,
    supplier: Suppliers,
) -> None:
    await session.delete(supplier)
    await session.commit()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from .schemas import InvoicesCreateSchema, InvoicesUpdateSchema, InvoicesSchema
from core.models import Invoices


async def get_all(
    session: AsyncSession,
) -> list[Invoices]:
    stmt = select(Invoices).execution_options(fresh=True)
    try:
        result = await session.execute(stmt)
        invoices_list = result.scalars().all()
        return invoices_list
    except Exception as e:
        print(f"Error fetching invoices: {str(e)}")
        raise


async def create(
    session: AsyncSession,
    invoice_in: InvoicesCreateSchema,
) -> Invoices:
    try:
        invoice = Invoices(**invoice_in.model_dump())
        session.add(invoice)
        await session.commit()
        await session.refresh(invoice)
        return invoice
    except Exception as e:
        print(f"Error creating invoice: {e}")
        raise e


async def get_by_id(
    session: AsyncSession,
    invoice_id: int,
) -> Invoices | None:
    stmt = (
        select(Invoices)
        .where(Invoices.id == invoice_id)
        .options(
            selectinload(Invoices.supplier),
        )
    )
    try:
        result = await session.execute(stmt)

        invoice = result.scalar_one_or_none()
        if invoice is None:
            return None
        return invoice
    except Exception as e:
        print(f"Error fetching invoice: {str(e)}")
        raise


async def update(
    session: AsyncSession,
    invoice: Invoices,
    invoice_update: InvoicesUpdateSchema,
) -> Invoices:
    for name, value in invoice_update.model_dump().items():
        setattr(invoice, name, value)
    await session.commit()
    await session.refresh(invoice)
    return invoice


async def delete(
    session: AsyncSession,
    invoice: Invoices,
) -> None:
    await session.delete(invoice)
    await session.commit()

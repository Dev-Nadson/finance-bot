from datetime import datetime, timedelta

from sqlalchemy import func, select

from database.models.db_config import get_session
from database.models.t04_expenses import Expenses
from database.models.t05_incomes import Incomes


async def calculate_balance(account_id: int):
    """Return (total_incomes, total_expenses, balance) for the given account."""
    async with get_session() as session:
        total_incomes_result = await session.execute(
            select(func.sum(Incomes.value)).filter_by(account_id=account_id)
        )
        total_incomes = total_incomes_result.scalar() or 0.0

        total_expenses_result = await session.execute(
            select(func.sum(Expenses.value)).filter_by(account_id=account_id)
        )
        total_expenses = total_expenses_result.scalar() or 0.0

        balance = total_incomes - total_expenses
        return total_incomes, total_expenses, balance, None


async def total_expenses_by_category(account_id: int) -> dict[str, float]:
    """Return a dict {category: total_value} for all expense categories of the account."""
    async with get_session() as session:
        rows = (
            await session.execute(
                select(Expenses.category, func.sum(Expenses.value))
                .filter_by(account_id=account_id)
                .group_by(Expenses.category)
            )
        ).all()

        return {row[0]: row[1] for row in rows if row[0]}


async def monthly_expenses_evolution(account_id: int, months: int = 6) -> tuple[list[str], list[float]]:
    """Return (month_labels, totals) for the last `months` months of expenses."""
    async with get_session() as session:
        cutoff = datetime.now() - timedelta(days=30 * months)
        rows = (
            await session.execute(
                select(
                    func.strftime("%Y-%m", Expenses.created_at).label("month"),
                    func.sum(Expenses.value).label("total"),
                )
                .filter(Expenses.account_id == account_id, Expenses.created_at >= cutoff)
                .group_by("month")
                .order_by("month")
            )
        ).all()

        labels = [row[0] for row in rows]
        totals = [row[1] or 0.0 for row in rows]
        return labels, totals


async def monthly_incomes_evolution(account_id: int, months: int = 6) -> tuple[list[str], list[float]]:
    """Return (month_labels, totals) for the last `months` months of incomes."""
    async with get_session() as session:
        cutoff = datetime.now() - timedelta(days=30 * months)
        rows = (
            await session.execute(
                select(
                    func.strftime("%Y-%m", Incomes.created_at).label("month"),
                    func.sum(Incomes.value).label("total"),
                )
                .filter(Incomes.account_id == account_id, Incomes.created_at >= cutoff)
                .group_by("month")
                .order_by("month")
            )
        ).all()

        labels = [row[0] for row in rows]
        totals = [row[1] or 0.0 for row in rows]
        return labels, totals

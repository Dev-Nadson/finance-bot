from datetime import datetime, timedelta

from sqlalchemy import func, select

from database.models.db_config import get_session
from database.models.t04_expenses import Expenses
from database.models.t05_incomes import Incomes


async def calculate_balance(account_id: int, month: int | None = None, year: int | None = None):
    """Return (total_incomes, total_expenses, balance) for the given account."""
    async with get_session() as session:
        from sqlalchemy import extract
        
        income_query = select(func.sum(Incomes.value)).filter(Incomes.account_id == account_id)
        expense_query = select(func.sum(Expenses.value)).filter(Expenses.account_id == account_id)

        if month is not None and year is not None:
            income_query = income_query.filter(extract('month', Incomes.created_at) == month)
            income_query = income_query.filter(extract('year', Incomes.created_at) == year)
            expense_query = expense_query.filter(extract('month', Expenses.created_at) == month)
            expense_query = expense_query.filter(extract('year', Expenses.created_at) == year)

        total_incomes_result = await session.execute(income_query)
        total_incomes = total_incomes_result.scalar() or 0.0

        total_expenses_result = await session.execute(expense_query)
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

from datetime import datetime, timedelta

from sqlalchemy import func, select

from database.models.db_config import get_session
from database.models.t04_expenses import Expenses
from database.models.t05_incomes import Incomes


async def calculate_balance(account_id: int, month: int | None = None, year: int | None = None):
    """Return (total_incomes, total_expenses, balance) for the given account."""
    async with get_session() as session:
        income_query = select(func.sum(Incomes.value)).filter(Incomes.account_id == account_id)
        expense_query = select(func.sum(Expenses.value)).filter(Expenses.account_id == account_id)

        if month is not None and year is not None:
            competencia_filter = f"{year:04d}-{month:02d}"
            income_query = income_query.filter(Incomes.competencia == competencia_filter)
            expense_query = expense_query.filter(Expenses.competencia == competencia_filter)

        total_incomes_result = await session.execute(income_query)
        total_incomes = total_incomes_result.scalar() or 0.0

        total_expenses_result = await session.execute(expense_query)
        total_expenses = total_expenses_result.scalar() or 0.0

        balance = total_incomes - total_expenses
        return total_incomes, total_expenses, balance, None


async def total_expenses_by_category(
    account_id: int, month: int | None = None, year: int | None = None
) -> dict[str, float]:
    """Return a dict {category: total_value} for all expense categories of the account."""
    async with get_session() as session:
        query = select(Expenses.category, func.sum(Expenses.value)).filter_by(account_id=account_id)

        if month is not None and year is not None:
            competencia_filter = f"{year:04d}-{month:02d}"
            query = query.filter(Expenses.competencia == competencia_filter)

        query = query.group_by(Expenses.category)

        rows = (await session.execute(query)).all()

        return {row[0]: row[1] for row in rows if row[0]}


async def monthly_expenses_evolution(account_id: int, months: int = 6) -> tuple[list[str], list[float]]:
    """Return (month_labels, totals) for the last `months` months of expenses."""
    async with get_session() as session:
        cutoff = datetime.now() - timedelta(days=30 * months)
        rows = (
            await session.execute(
                select(
                    Expenses.competencia.label("month"),
                    func.sum(Expenses.value).label("total"),
                )
                .filter(
                    Expenses.account_id == account_id,
                    Expenses.competencia.isnot(None),
                    Expenses.competencia >= cutoff.strftime("%Y-%m"),
                )
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
                    Incomes.competencia.label("month"),
                    func.sum(Incomes.value).label("total"),
                )
                .filter(
                    Incomes.account_id == account_id,
                    Incomes.competencia.isnot(None),
                    Incomes.competencia >= cutoff.strftime("%Y-%m"),
                )
                .group_by("month")
                .order_by("month")
            )
        ).all()

        labels = [row[0] for row in rows]
        totals = [row[1] or 0.0 for row in rows]
        return labels, totals

from services.controllers.expense_controller import list_expenses
from services.controllers.income_controller import list_incomes


async def calculate_balance(telegram_id: str):
    incomes, i_error = await list_incomes(telegram_id)
    expenses, e_error = await list_expenses(telegram_id)

    if i_error or e_error:
        error_msg = f"{i_error or ''} {e_error or ''}".strip()
        return 0, 0, 0, error_msg

    total_incomes = sum([inc.get("value", 0) for inc in incomes])
    total_expenses = sum([exp.get("value", 0) for exp in expenses])

    balance = total_incomes - total_expenses

    return total_incomes, total_expenses, balance, None

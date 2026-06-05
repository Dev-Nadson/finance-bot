from services.controllers.login_controller import _ensure_active_account
from services.financeiro import calculate_balance as _calculate_balance


async def calculate_balance(telegram_id: int | str, context=None, month: int | None = None, year: int | None = None):
    """Calculate balance for the active account of the user."""
    account_id = None
    if context is not None:
        account_id = await _ensure_active_account(telegram_id, context)

    if account_id is None:
        return 0, 0, 0, "Nenhuma conta ativa encontrada."

    return await _calculate_balance(account_id, month=month, year=year)

from datetime import datetime
import asyncio
from config.libs.openapi_config import generate_gpt_response
from services.financeiro import calculate_balance
from services.repositories.expenses_repository import list_expenses_repo


async def generate_financial_report(telegram_id: str, account_id: int, month: int, year: int) -> str:
    """Generate a financial report using AI based on the user's monthly data."""
    
    # 1. Fetch balance data
    incomes, expenses, balance, err = await calculate_balance(account_id, month=month, year=year)
    if err:
        return f"Erro ao coletar dados para o relatório: {err}"

    # 2. Fetch expenses by category
    all_exps, _ = await list_expenses_repo(telegram_id, account_id, month=month, year=year)
    
    categories = {}
    for e in all_exps:
        cat = e.get("category", "Outros")
        categories[cat] = categories.get(cat, 0) + e.get("value", 0)

    # 3. Build Prompt
    month_name = datetime(year, month, 1).strftime("%B/%Y")
    
    cat_summary = "\n".join([f"- {cat}: R$ {val:.2f}" for cat, val in categories.items()])
    
    prompt = f"""
    Analise os seguintes dados financeiros do mês de {month_name}:
    - Receitas Totais: R$ {incomes:.2f}
    - Despesas Totais: R$ {expenses:.2f}
    - Saldo Final: R$ {balance:.2f}
    
    Despesas por Categoria:
    {cat_summary if cat_summary else "Nenhuma despesa registrada."}
    
    Por favor, forneça:
    1. Um resumo curto da situação financeira do mês.
    2. Identifique onde o usuário mais gastou.
    3. Dê 3 dicas práticas e curtas de como economizar ou investir melhor bases nestes dados.
    
    Seja amigável e direto. Use tags HTML (<b> para negrito, <i> para itálico) em vez de Markdown. Não use códigos ou blocos complexos.
    """

    # 4. Generate Response
    response = await asyncio.to_thread(generate_gpt_response, prompt)
    
    header = f"🤖 <b>Relatório de IA — {month_name}</b>\n\n"
    # Basic cleanup for HTML safety
    response = response.replace("<br>", "\n").replace("<p>", "").replace("</p>", "\n")
    return header + response

import sys
import asyncio
from pathlib import Path
import io

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from flask import Flask, render_template, send_file, request, jsonify
from datetime import datetime

from config.schemas.classes import ChartLinesData, ChartPieData
from services.reports.charts import generate_lines_chart, generate_pie_chart
from services.financeiro import (
    calculate_balance, 
    total_expenses_by_category, 
    monthly_expenses_evolution, 
    monthly_incomes_evolution
)
from database.models.db_config import get_session
from database.models.t02_accounts import Account
from database.models.t01_users import User
from sqlalchemy import select

app = Flask(__name__)

def get_default_account():
    async def _get():
        async with get_session() as session:
            acc = (await session.execute(select(Account))).scalars().first()
            user = (await session.execute(select(User))).scalars().first()
            return acc, user
    return asyncio.run(_get())


@app.route("/")
def home():
    acc, user = get_default_account()
    if not acc:
        return "Nenhuma conta encontrada no banco de dados para exibir o dashboard."
    
    account_id = acc.account_id
    now = datetime.now()
    
    async def fetch_data():
        incomes, expenses, balance, _ = await calculate_balance(account_id, now.month, now.year)
        return incomes, expenses, balance

    incomes, expenses, balance = asyncio.run(fetch_data())
    
    return render_template(
        "index.html", 
        account_name=acc.name, 
        incomes=incomes, 
        expenses=expenses, 
        balance=balance,
        month=now.strftime("%m/%Y"),
        account_id=account_id,
        telegram_id=user.telegram_id if user else ""
    )


@app.route("/api/insights")
def api_insights():
    account_id = request.args.get("account_id", type=int)
    telegram_id = request.args.get("telegram_id", type=str)
    now = datetime.now()
    
    if not account_id or not telegram_id:
        return jsonify({"error": "Parâmetros ausentes"})
        
    from services.controllers.ai_controller import generate_financial_report
    
    async def fetch():
        return await generate_financial_report(telegram_id, account_id, now.month, now.year)
        
    try:
        report = asyncio.run(fetch())
        return jsonify({"report": report})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/graficos")
def graficos():
    return render_template("index.html")


@app.route("/despesas")
def despesas():
    acc, _ = get_default_account()
    if not acc: return ""
    
    async def fetch():
        return await monthly_expenses_evolution(acc.account_id)
        
    labels, totals = asyncio.run(fetch())
    if not labels:
        labels, totals = ["N/A"], [0]
        
    chart = generate_lines_chart(
        ChartLinesData(
            title="Evolução de Despesas",
            x_values=labels,
            y_values=totals,
            xlabel="Mês",
            ylabel="Valor R$",
        )
    )
    return send_file(io.BytesIO(chart), mimetype="image/png")


@app.route("/receitas")
def receitas():
    acc, _ = get_default_account()
    if not acc: return ""
    
    async def fetch():
        return await monthly_incomes_evolution(acc.account_id)
        
    labels, totals = asyncio.run(fetch())
    if not labels:
        labels, totals = ["N/A"], [0]

    chart = generate_lines_chart(
        ChartLinesData(
            title="Evolução de Receitas",
            x_values=labels,
            y_values=totals,
            xlabel="Mês",
            ylabel="Valor R$",
        )
    )
    return send_file(io.BytesIO(chart), mimetype="image/png")


@app.route("/pizza")
def pizza():
    acc, _ = get_default_account()
    if not acc: return ""
    
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    
    async def fetch():
        return await total_expenses_by_category(acc.account_id, month=month, year=year)
        
    category_data = asyncio.run(fetch())
    if not category_data:
        category_data = {"N/A": 0}
        
    chart = generate_pie_chart(
        ChartPieData(
            title="Despesas por Categoria",
            categories=list(category_data.keys()),
            values=list(category_data.values()),
        )
    )
    return send_file(io.BytesIO(chart), mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)

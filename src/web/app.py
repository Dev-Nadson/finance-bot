import sys
from pathlib import Path
import io

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from flask import Flask, render_template, send_file

from config.schemas.classes import ChartLinesData, ChartPieData
from services.reports.charts import generate_lines_chart, generate_pie_chart

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/graficos")
def graficos():
    return render_template("index.html")


@app.route("/despesas")
def despesas():
    chart = generate_lines_chart(
        ChartLinesData(
            title="Despesas Mensais",
            x_values=["Jan", "Fev", "Mar", "Abr"],
            y_values=[300, 450, 280, 600],
            xlabel="Mês",
            ylabel="Valor R$",
        )
    )

    return send_file(
        io.BytesIO(chart),
        mimetype="image/png"
    )


@app.route("/receitas")
def receitas():
    chart = generate_lines_chart(
        ChartLinesData(
            title="Receitas Mensais",
            x_values=["Jan", "Fev", "Mar", "Abr"],
            y_values=[1000, 1200, 900, 1500],
            xlabel="Mês",
            ylabel="Valor R$",
        )
    )

    return send_file(
        io.BytesIO(chart),
        mimetype="image/png"
    )


@app.route("/pizza")
def pizza():
    chart = generate_pie_chart(
        ChartPieData(
            title="Despesas por Categoria",
            categories=["Alimentação", "Transporte", "Lazer", "Educação"],
            values=[25, 35, 20, 20],
        )
    )

    return send_file(
        io.BytesIO(chart),
        mimetype="image/png"
    )


if __name__ == "__main__":
    app.run(debug=True)
import io
from matplotlib.figure import Figure
from config.schemas.classes import ChartLinesData, ChartPieData

def generate_lines_chart(data: ChartLinesData) -> bytes:
    fig = Figure(figsize=(8, 5))
    ax = fig.subplots()

    ax.plot(data.x_values, data.y_values, linestyle='--', marker='o', color='blue')
    ax.set(
        xlabel=data.xlabel,
        ylabel=data.ylabel,
        title=data.title
    )
    ax.grid(True)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    return buf.getvalue()


def generate_pie_chart(data: ChartPieData) -> bytes:
    fig = Figure(figsize=(8, 5))
    ax = fig.subplots()

    ax.pie(data.values, labels=data.categories, autopct='%1.1f%%')
    ax.set(
        title=data.title
    )
    ax.grid(True)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    return buf.getvalue()
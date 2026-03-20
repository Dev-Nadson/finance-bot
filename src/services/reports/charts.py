import io

import matplotlib

# from config.schemas.classes import ChartLinesData, ChartPieData
import numpy as np
from matplotlib.figure import Figure

matplotlib.use("Agg")
from dataclasses import dataclass, field
from typing import List

import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch


@dataclass
class ChartLinesData:
    title: str
    x_values: List
    y_values: List  # lista simples OU lista de listas (múltiplas séries)
    xlabel: str = ""
    ylabel: str = ""
    series_labels: List[str] = field(default_factory=list)


def generate_lines_chart(data: ChartLinesData) -> bytes:
    # ── Paleta (mesma do pie chart) ─────────────────────────────────────────
    BG = "#0D0D0D"
    TITLE_COLOR = "#FFFFFF"
    LABEL_COLOR = "#C8C8C8"
    TICK_COLOR = "#888888"
    SPINE_COLOR = "#2A2A3A"

    LINE_COLORS = [
        "#2979FF",  # azul elétrico
        "#E040FB",  # magenta
        "#76FF03",  # verde-limão
        "#FF6D00",  # laranja
        "#AA00FF",  # roxo
        "#FFD600",  # amarelo
    ]

    # Normaliza: aceita série única ou múltiplas séries
    if data.y_values and not isinstance(data.y_values[0], (list, np.ndarray)):
        all_series = [data.y_values]
    else:
        all_series = data.y_values

    n_series = len(all_series)
    has_legend = bool(data.series_labels) and n_series > 1

    # ── Figura ──────────────────────────────────────────────────────────────
    fig = Figure(figsize=(12, 6), facecolor=BG, dpi=130)

    # ── Grid de fundo cobrindo TODA a figura ────────────────────────────────
    grid_ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], zorder=0)
    grid_ax.set_facecolor(BG)
    grid_ax.set_xlim(0, 1)
    grid_ax.set_ylim(0, 1)
    grid_ax.set_axis_off()

    # Linhas finas (subdivisão densa)
    minor_kw = dict(color="#1A1A2A", lw=0.45, alpha=0.75, zorder=0)
    for x in np.arange(0, 1.001, 0.025):
        grid_ax.axvline(x, **minor_kw)
    for y in np.arange(0, 1.001, 0.025):
        grid_ax.axhline(y, **minor_kw)

    # Linhas maiores com toque azulado
    major_kw = dict(color="#1E2840", lw=0.9, alpha=0.9, zorder=1)
    for x in np.arange(0, 1.001, 0.1):
        grid_ax.axvline(x, **major_kw)
    for y in np.arange(0, 1.001, 0.1):
        grid_ax.axhline(y, **major_kw)

    # ── Eixo do gráfico (sobre o grid) ──────────────────────────────────────
    right_margin = 0.30 if has_legend else 0.04
    ax = fig.add_axes([0.09, 0.12, 0.87 - right_margin, 0.76], zorder=2)
    ax.set_facecolor("none")

    # ── Desenho das séries ───────────────────────────────────────────────────
    line_objects = []
    for i, y_vals in enumerate(all_series):
        color = LINE_COLORS[i % len(LINE_COLORS)]

        # Área preenchida com gradiente sutil sob a linha
        ax.fill_between(
            data.x_values,
            y_vals,
            alpha=0.08,
            color=color,
            zorder=2,
        )

        # Linha principal com glow (stroke duplo)
        (line_glow,) = ax.plot(
            data.x_values,
            y_vals,
            linestyle="-",
            color=color,
            linewidth=4.5,
            alpha=0.25,
            zorder=3,
        )

        (line,) = ax.plot(
            data.x_values,
            y_vals,
            linestyle="-",
            marker="o",
            color=color,
            linewidth=2.0,
            markersize=7,
            markerfacecolor=BG,
            markeredgecolor=color,
            markeredgewidth=2.0,
            zorder=4,
            label=data.series_labels[i] if data.series_labels and i < len(data.series_labels) else None,
        )
        line_objects.append(line)

        # Valor em cada ponto
        for xi, yi in zip(data.x_values, y_vals):
            ax.annotate(
                f"{yi:g}",
                xy=(xi, yi),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                color=color,
                fontweight="bold",
                path_effects=[pe.withStroke(linewidth=2.5, foreground=BG)],
                zorder=5,
            )

    # ── Estilo dos eixos ─────────────────────────────────────────────────────
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_color(SPINE_COLOR)
        ax.spines[side].set_linewidth(0.8)

    ax.tick_params(colors=TICK_COLOR, labelsize=9, length=4, width=0.7)
    ax.set_xlabel(data.xlabel, fontsize=11, color=LABEL_COLOR, labelpad=10)
    ax.set_ylabel(data.ylabel, fontsize=11, color=LABEL_COLOR, labelpad=10)

    # Padding superior para os valores não cortarem
    y_all = [v for s in all_series for v in s]
    y_range = max(y_all) - min(y_all) if max(y_all) != min(y_all) else 1
    ax.set_ylim(min(y_all) - y_range * 0.12, max(y_all) + y_range * 0.22)

    # ── Título ───────────────────────────────────────────────────────────────
    fig.text(
        0.5,
        0.97,
        data.title.upper(),
        ha="center",
        va="top",
        fontsize=14,
        color=TITLE_COLOR,
        fontweight="black",
        alpha=0.95,
        transform=fig.transFigure,
        path_effects=[pe.withStroke(linewidth=4, foreground=BG)],
    )

    # ── Legenda lateral (só quando há múltiplas séries) ──────────────────────
    if has_legend:
        legend_ax = fig.add_axes([0.73, 0.25, 0.25, 0.50], zorder=3)
        legend_ax.set_facecolor("none")
        legend_ax.set_xlim(0, 1)
        legend_ax.set_ylim(0, 1)
        legend_ax.set_axis_off()

        box = FancyBboxPatch(
            (0.0, 0.0),
            1.0,
            1.0,
            boxstyle="round,pad=0.02",
            linewidth=1.2,
            edgecolor="#2E2E2E",
            facecolor="#12121E",
            alpha=0.92,
            transform=legend_ax.transAxes,
            zorder=0,
        )
        legend_ax.add_patch(box)

        legend_ax.text(
            0.5,
            0.90,
            "Séries",
            ha="center",
            va="center",
            fontsize=10,
            color="white",
            fontweight="bold",
            transform=legend_ax.transAxes,
        )
        legend_ax.axhline(y=0.82, xmin=0.05, xmax=0.95, color="#2E2E2E", linewidth=0.8)

        row_h = 0.65 / n_series
        for i, label in enumerate(data.series_labels[:n_series]):
            color = LINE_COLORS[i % len(LINE_COLORS)]
            y_pos = 0.76 - i * row_h - row_h / 2

            # Linha colorida pequena como marcador
            legend_ax.plot(
                [0.07, 0.22],
                [y_pos, y_pos],
                color=color,
                lw=2.2,
                transform=legend_ax.transAxes,
                zorder=2,
            )
            legend_ax.plot(
                [0.145],
                [y_pos],
                marker="o",
                color=BG,
                markeredgecolor=color,
                markeredgewidth=1.8,
                markersize=5,
                transform=legend_ax.transAxes,
                zorder=3,
            )
            legend_ax.text(
                0.30,
                y_pos,
                label,
                ha="left",
                va="center",
                fontsize=9,
                color="#D0D0D0",
                transform=legend_ax.transAxes,
            )

    # ── Decoração ────────────────────────────────────────────────────────────
    fig.text(0.97, 0.03, "✦", ha="right", va="bottom", fontsize=18, color="#2A2A3A", transform=fig.transFigure)

    # ── Exportar ─────────────────────────────────────────────────────────────
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor=BG, edgecolor="none")
    buf.seek(0)
    return buf.getvalue()


# ── Exemplo de uso ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Série única
    sample_single = ChartLinesData(
        title="Receita Mensal 2024",
        x_values=["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        y_values=[42, 58, 51, 67, 74, 88, 95, 82, 99, 110, 104, 130],
        xlabel="Mês",
        ylabel="Receita (k R$)",
    )

    with open("lines_single.png", "wb") as f:
        f.write(generate_lines_chart(sample_single))
    print("✅ lines_single.png")

    # Múltiplas séries
    sample_multi = ChartLinesData(
        title="Vendas por Canal — 2024",
        x_values=["Q1", "Q2", "Q3", "Q4"],
        y_values=[
            [120, 145, 162, 190],
            [80, 95, 110, 140],
            [55, 70, 88, 105],
        ],
        xlabel="Trimestre",
        ylabel="Unidades",
        series_labels=["Online", "Loja Física", "Parceiros"],
    )

    with open("lines_multi.png", "wb") as f:
        f.write(generate_lines_chart(sample_multi))
    print("✅ lines_multi.png")


import matplotlib

matplotlib.use("Agg")
from dataclasses import dataclass
from typing import List


@dataclass
class ChartData:
    title: str
    categories: List[str]
    values: List[float]


def generate_pie_chart(data: ChartData) -> bytes:
    # ── Paleta inspirada na imagem ──────────────────────────────────────────
    BG = "#0D0D0D"  # fundo quase preto
    GRID_COLOR = "#1E1E1E"  # grid sutilíssimo
    LABEL_COLOR = "#C8C8C8"  # labels externos
    TITLE_COLOR = "#FFFFFF"

    # Cores das fatias (mesma ordem visual da imagem)
    SLICE_COLORS = [
        "#2979FF",  # Vendas     – azul elétrico
        "#E040FB",  # Marketing  – magenta/violeta
        "#76FF03",  # Pesquisa   – verde-limão
        "#FF6D00",  # Despesas   – laranja
        "#AA00FF",  # Operações  – roxo profundo
        "#FFD600",  # extra
    ]

    n = len(data.values)
    colors = SLICE_COLORS[:n]

    # ── Figura ──────────────────────────────────────────────────────────────
    fig = Figure(figsize=(13, 6.5), facecolor=BG, dpi=130)

    # ── Grid de fundo cobrindo TODA a figura ────────────────────────────────
    grid_ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], zorder=0)
    grid_ax.set_facecolor(BG)
    grid_ax.set_xlim(0, 1)
    grid_ax.set_ylim(0, 1)
    grid_ax.set_axis_off()

    # Linhas finas – subdivisão densa (passo 0.025)
    minor_kw = dict(color="#1A1A2A", lw=0.45, alpha=0.75, zorder=0)
    for x in np.arange(0, 1.001, 0.025):
        grid_ax.axvline(x, **minor_kw)
    for y in np.arange(0, 1.001, 0.025):
        grid_ax.axhline(y, **minor_kw)

    # Linhas maiores – grade 10×10 com leve toque azulado
    major_kw = dict(color="#1E2840", lw=0.9, alpha=0.9, zorder=1)
    for x in np.arange(0, 1.001, 0.1):
        grid_ax.axvline(x, **major_kw)
    for y in np.arange(0, 1.001, 0.1):
        grid_ax.axhline(y, **major_kw)

    # ── Eixo da pizza (sobre o grid, fundo transparente) ───────────────────
    ax = fig.add_axes([0.02, 0.02, 0.62, 0.92], zorder=2)
    ax.set_facecolor("none")
    ax.set_axis_on()
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ── Pizza ───────────────────────────────────────────────────────────────
    explode = [0.04] * n

    wedges, _, autotexts = ax.pie(
        data.values,
        explode=explode,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        pctdistance=0.70,
        wedgeprops={
            "edgecolor": BG,
            "linewidth": 2.0,
            "antialiased": True,
        },
        textprops={"color": "white", "weight": "bold", "fontsize": 11},
    )

    # Sombra nos textos de porcentagem
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("black")
        at.set_path_effects(
            [
                pe.withStroke(linewidth=3, foreground=BG),
            ]
        )

    # ── Labels externos (como na imagem) ────────────────────────────────────
    for i, (wedge, label) in enumerate(zip(wedges, data.categories)):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = np.cos(np.radians(angle))
        y = np.sin(np.radians(angle))

        label_dist = 1.28
        lx = label_dist * x
        ly = label_dist * y

        ha = "left" if x >= 0 else "right"

        ax.annotate(
            label,
            xy=(0.90 * x, 0.90 * y),
            xytext=(lx, ly),
            ha=ha,
            va="center",
            fontsize=9.5,
            color=LABEL_COLOR,
            fontweight="normal",
            arrowprops=dict(
                arrowstyle="-",
                color="#3A3A3A",
                lw=0.8,
            ),
        )

    # ── Título ───────────────────────────────────────────────────────────────
    fig.text(
        0.35,
        0.97,
        data.title.upper(),
        ha="center",
        va="top",
        fontsize=14,
        color=TITLE_COLOR,
        fontweight="black",
        fontfamily="DejaVu Sans",
        alpha=0.95,
        transform=fig.transFigure,
    )

    # ── Legenda lateral customizada ──────────────────────────────────────────
    legend_ax = fig.add_axes([0.65, 0.15, 0.33, 0.65], zorder=3)
    legend_ax.set_facecolor("none")
    legend_ax.set_xlim(0, 1)
    legend_ax.set_ylim(0, 1)
    legend_ax.set_axis_off()

    # Borda da caixa de legenda
    box = FancyBboxPatch(
        (0.0, 0.0),
        1.0,
        1.0,
        boxstyle="round,pad=0.02",
        linewidth=1.2,
        edgecolor="#2E2E2E",
        facecolor="#161616",
        transform=legend_ax.transAxes,
        zorder=0,
    )
    legend_ax.add_patch(box)

    # Título da legenda
    legend_ax.text(
        0.5,
        0.90,
        "Categorias",
        ha="center",
        va="center",
        fontsize=11,
        color="white",
        fontweight="bold",
        transform=legend_ax.transAxes,
    )

    # Linha separadora
    legend_ax.axhline(
        y=0.82,
        xmin=0.05,
        xmax=0.95,
        color="#2E2E2E",
        linewidth=0.8,
    )

    # Itens
    row_height = 0.68 / n
    for i, (cat, color) in enumerate(zip(data.categories, colors)):
        y_pos = 0.76 - i * row_height - row_height / 2

        # Quadrado colorido
        rect = FancyBboxPatch(
            (0.07, y_pos - 0.045),
            0.12,
            0.085,
            boxstyle="round,pad=0.01",
            facecolor=color,
            edgecolor="none",
            transform=legend_ax.transAxes,
            zorder=2,
        )
        legend_ax.add_patch(rect)

        # Texto
        legend_ax.text(
            0.26,
            y_pos,
            cat,
            ha="left",
            va="center",
            fontsize=10,
            color="#D0D0D0",
            transform=legend_ax.transAxes,
        )

    # ── Decoração: estrela (sparkle) ─────────────────────────────────────────
    fig.text(
        0.96,
        0.04,
        "✦",
        ha="right",
        va="bottom",
        fontsize=18,
        color="#333333",
        transform=fig.transFigure,
    )

    # ── Exportar ─────────────────────────────────────────────────────────────
    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        bbox_inches="tight",
        dpi=130,
        facecolor=BG,
        edgecolor="none",
    )
    buf.seek(0)
    return buf.getvalue()


# ── Exemplo de uso ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = ChartData(
        title="Distribuição de Recursos no Quadrimestre",
        categories=["Vendas", "Marketing", "Pesquisa", "Despesas", "Operações"],
        values=[30.1, 25.4, 18.2, 15.3, 11.0],
    )

    png_bytes = generate_pie_chart(sample)

    with open("chart_output.png", "wb") as f:
        f.write(png_bytes)

    print("✅ Gráfico gerado: chart_output.png")

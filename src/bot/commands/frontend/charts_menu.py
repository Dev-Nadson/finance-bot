from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def charts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🥧 Despesas por Categoria", callback_data="chart_pie_expenses")],
            [InlineKeyboardButton("📈 Evolução de Despesas", callback_data="chart_line_expenses")],
            [InlineKeyboardButton("📈 Evolução de Receitas", callback_data="chart_line_incomes")],
            [InlineKeyboardButton("🔙 Voltar", callback_data="menu_main")],
        ]
    )
    text = "📊 *Gráficos*\n\nEscolha o gráfico:"
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")


async def handle_charts_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fallback handler — chart callbacks are now handled by handle_callback in show_menu."""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Use /menu → Gráficos para visualizar seus dados.")

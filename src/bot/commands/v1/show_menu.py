from bot.setup import bot
from telebot import types

def show_menu(msg: types.Message):
    markup =    types.InlineKeyboardMarkup(row_width=1)

    btn_despesas = types.InlineKeyboardButton("💸 Registar Despesas", callback_data = "add_despesa" )
    btn_receitas = types.InlineKeyboardButton("💰 Registrar Receitas", callback_data = "add_receitas")
    btn_balance = types.InlineKeyboardButton("📊 Calcular Saldo", callback_data = "show_balance")

    markup.add(btn_despesas,btn_balance,btn_receitas)

    bot_reply_to(msg, "Olá! Escolha uma das opções abaixo para gerir suas finanças: ", reply_markup=markup)

def handle_callback(call, bot):
    if call.data == "add_despesas":
        bot.send.Message(call.message.chat.id, "Digite o Valor da Despesa:")
    elif call.data = "ver_saldo"
        bot.send.Message(call.message.chat.id, "Consultando seu saldo nos Registros...")

    bot_answer_callback_query(call.id)

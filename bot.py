import time

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import token
from logic import TextAnalysis


bot = telebot.TeleBot(token)


def get_owner(user):
    return user.username or str(user.id)


def send_with_typing(chat_id, text, reply_markup=None):
    bot.send_chat_action(chat_id, "typing")
    time.sleep(1)
    bot.send_message(chat_id, text, reply_markup=reply_markup)


def gen_markup_for_text():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Получить ответ", callback_data="text_ans"),
        InlineKeyboardButton("Перевести сообщение", callback_data="text_translate"),
    )
    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith("text"))
def callback_query(call):
    owner = get_owner(call.from_user)
    history = TextAnalysis.memory[owner]

    if not history:
        bot.answer_callback_query(call.id, "Сначала отправь сообщение.")
        return

    obj = history[-1]

    if call.data == "text_ans":
        send_with_typing(call.message.chat.id, obj.response)
    elif call.data == "text_translate":
        send_with_typing(call.message.chat.id, obj.translation)

    bot.answer_callback_query(call.id)


@bot.message_handler(commands=["start"])
def start_message(message):
    send_with_typing(
        message.chat.id,
        "Привет! Отправь мне текст, и я предложу, что с ним сделать.",
    )


@bot.message_handler(content_types=["text"])
def handle_message(message):
    TextAnalysis(message.text, get_owner(message.from_user))
    send_with_typing(
        message.chat.id,
        "Я получил твое сообщение! Что ты хочешь с ним сделать?",
        reply_markup=gen_markup_for_text(),
    )


def run_bot():
    bot.infinity_polling(none_stop=True)

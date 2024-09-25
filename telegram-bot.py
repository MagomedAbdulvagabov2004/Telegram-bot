import logging
import re

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

TOKEN = "7272467040:AAGAiv-aw2NvY3zCh3xfmai2G-eVENgMMDg"  # Замените на ваш токен бота

# Подключаем логирование
logging.basicConfig(
    filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Состояния диалога
FIND_EMAIL = range(1)
FIND_PHONE_NUMBER = range(1)

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}! Я могу искать email адреса и номера телефонов в тексте.\n'
                             f'Введите команду /find_email или /find_phone_number.')


def find_email(update: Update, context):
    """Обработчик команды /find_email."""
    update.message.reply_text('Введите текст, в котором нужно найти email адреса:')
    return FIND_EMAIL


def find_email_handler(update: Update, context):
    """Обработчик текста после команды /find_email."""
    user_input = update.message.text
    email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    email_list = re.findall(email_regex, user_input)
    if email_list:
        update.message.reply_text(f"Найденные email адреса: {'/n'.join(email_list)}")
    else:
        update.message.reply_text("Email адреса не найдены.")
    return ConversationHandler.END


def find_phone_number(update: Update, context):
    """Обработчик команды /find_phone_number."""
    update.message.reply_text('Введите текст, в котором нужно найти номера телефонов:')
    return FIND_PHONE_NUMBER


def find_phone_number_handler(update: Update, context):
    """Обработчик текста после команды /find_phone_number."""
    user_input = update.message.text
    phone_regex = r"((?:\+7|8)?[\s-]?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2}))"
    phone_list = re.findall(phone_regex, user_input)
    if phone_list:
        update.message.reply_text(f"Найденные номера телефонов:\n{'\n'.join(f'+7 ({phone[1]}) {phone[2]}-{phone[3]}-{phone[4]}' for phone in phone_list)}")
    else:
        update.message.reply_text("Номера телефонов не найдены.")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('find_email', find_email)],
        states={
            FIND_EMAIL: [MessageHandler(Filters.text & ~Filters.command, find_email_handler)]
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', find_phone_number)],
        states={
            FIND_PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, find_phone_number_handler)]
        },
        fallbacks=[]
    ))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
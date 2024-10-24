import logging
import queue
import time
import psycopg2
from pydantic.v1.networks import host_regex
from questionary import password
from telegram import Update, Bot
import re
from telegram import Update, Bot
from telegram.ext import (
  Updater,
  CommandHandler,
  MessageHandler,
  Filters, ConversationHandler,
)

# Настройка логгирования
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота
BOT_TOKEN = "2127491244:AAFLKvfN1grM8aR0gmzRqrShJo7IJHuKAX8" # Замените на ваш токен

# Параметры подключения к PostgreSQL
DB_HOST = "localhost"
DB_NAME = "users"
DB_USER = "postgres"
DB_PASSWORD = "79EaSc##"


# Регулярные выражения для поиска телефонов и почты
phone_regex = r"((?:\+7|8)?[\s-]?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2}))" # Телефон
email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)" # Почта

# Файл с данными
FILE_PATH = "C:/Users/User/Desktop/ReceivedFile.txt" # Замените на путь к вашему файлу


# Состояние диалога
WRITE_EMAILS = range(1)
WRITE_PHONE_NUMBERS = range(1)
FIND_EMAIL = range(1)
FIND_PHONE_NUMBER = range(1)
VERIFY_PASSWORD = range(1)


# Инициализация бота
bot = Bot(token=BOT_TOKEN)

def start(update, context):
  """Отправляет приветственное сообщение."""
  bot.send_message(chat_id=update.message.chat_id, text="Привет! Вот что я умею:\n\n"
                                                        "1) Находить почты и номера телефонов в текстовом файле\n\n"
                                                        "2) Находить почты и номера телефонов в тексте, команда: /find_email /find_phone_numbers\n\n"
                                                        "3) Проверять пароль на сложность, команда: /verify_password\n\n"
                                                        "4) Извлекать номера телефонов и почты из Базы Данных, команды: /get_emails, /get_phone_numbers\n\n"
                                                        "5) Записывать номера телефонов и почты в Базу Данных, команды: /save_emails, /save_phone_numbers")


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
        update.message.reply_text(f"Найденные email адреса:\n{'\n'.join(email_list)}")
    else:
        update.message.reply_text("Email адреса не найдены.")
    return ConversationHandler.END

def verify_password_handler(update: Update, context):
    """Обработчик команды /verify_password."""
    update.message.reply_text('Введите пароль: ')
    return VERIFY_PASSWORD

def check_password(update: Update, context):
    digits = '1234567890'
    upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_letters = 'abcdefghijklmnopqrstuvwxyz'
    symbols = '!@#$%^&*()-+'
    acceptable = digits + upper_letters + lower_letters + symbols

    verdict_final = ''

    # passwd = set(context)
    if any(char not in acceptable for char in context):
        print('Ошибка. Запрещенный спецсимвол')
    else:
        recommendations = []
        if len(context) < 12:
            recommendations.append(f'увеличить число символов - {12 - len(context)}')
        for what, message in ((digits, 'цифру'),
                              (symbols, 'спецсимвол'),
                              (upper_letters, 'заглавную букву'),
                              (lower_letters, 'строчную букву')):
            if all(char not in what for char in context):
                recommendations.append(f'добавить 1 {message}')

        if recommendations:
            verdict_final = "Слабый пароль. Рекомендации:", ", ".join(recommendations)
            print("Слабый пароль. Рекомендации:", ", ".join(recommendations))
        else:
            verdict_final = 'Сильный пароль.'
            print('Сильный пароль.')

    update.message.reply_text(verdict_final)
    return ConversationHandler.END

def verify_password(update: Update, context):

    verdict = ''

    if len(update.message.text) < 8:
        verdict = "Пароль слишком короткий"

    if not re.search("[A-Z]", update.message.text):
        verdict = "Пароль должен содержать хотя бы одну Заглавную букву"

    if not re.search("[a-z]", update.message.text):
        verdict = "Пароль долже содержать хотя бы одну строчную букву"

    if not re.search("[0-9]", update.message.text):
        verdict = "Пароль должен содержать хотя бы одну цифру"

    if not re.search("[!@#$%^&*()]", update.message.text):
        verdict = "Пароль слишком простой"
    else:
        verdict = "Пароль сложный"


    update.message.reply_text(verdict)

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

def get_emails(update: Update, context):
    """Обрабатывает команду /get_emails."""
    chat_id = update.message.chat_id
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM emails")
        emails = [row[0] for row in cursor.fetchall()]
        if emails:
            message = f"Найденные email адреса:\n{', '.join(emails)}"
        else:
            message = "Email адреса не найдены."
        bot.send_message(chat_id=chat_id, text=message)
        conn.close()
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"Ошибка: {e}")


def get_phone_numbers(update: Update, context):
    """Обрабатывает команду /get_phone_numbers."""
    chat_id = update.message.chat_id
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number FROM phone_numbers")
        phone_numbers = [row[0] for row in cursor.fetchall()]
        if phone_numbers:
            message = f"Найденные телефонные номера:\n{', '.join(phone_numbers)}"
        else:
            message = "Телефонные номера не найдены."
        bot.send_message(chat_id=chat_id, text=message)
        conn.close()
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"Ошибка: {e}")


def save_emails(update: Update, context):
    chat_id = update.message.chat_id
    # user_data["chat_id"] = chat_id
    bot.send_message(
        chat_id, text="Введите почты для их записи в БД:",
    )
    return WRITE_EMAILS

def save_emails_handler(update: Update, context):
    chat_id = update.message.chat_id
    search_text = update.message.text
    email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    email_list = re.findall(email_regex, search_text)
    if email_list:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
            cursor = conn.cursor()
            for email in email_list:
                cursor.execute(f"INSERT INTO emails (email) VALUES ('{email}')")
            conn.commit()
            bot.send_message(chat_id=chat_id, text="Email адреса успешно записаны.")
            conn.close()
        except Exception as e:
            bot.send_message(chat_id=chat_id, text=f"Ошибка при записи: {e}")
    else:
        bot.send_message(chat_id=chat_id, text=f"Email адреса не найдены!")

    return ConversationHandler.END

def save_phone_numbers(update: Update, context):
  chat_id = update.message.chat_id
  # user_data["chat_id"] = chat_id
  bot.send_message(
    chat_id, text="Введите номера телефонов для их записи в БД: ",
  )
  return WRITE_PHONE_NUMBERS

def save_phone_numbers_handler(update: Update, context):
  chat_id = update.message.chat_id
  search_text = update.message.text
  phone_numbers_regex = r"((?:\+7|8)?[\s-]?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2}))"
  phone_numbers_list = re.findall(phone_numbers_regex, search_text)
  try:
    conn = psycopg2.connect(
      host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cursor = conn.cursor()
    for phone_number in phone_numbers_list:
      cursor.execute(f"INSERT INTO phone_numbers (phone_number) VALUES ('{phone_number[0]}')")
    conn.commit()
    bot.send_message(chat_id, text="Телефонные номера успешны записаны.")
    conn.close()

  except Exception as e:
    bot.send_message(chat_id, text=f"Ошибка при записи: {e}")

  return ConversationHandler.END

def handle_document(update, context):
  """Обрабатывает входящий файл."""
  file_id = update.message.document.file_id
  file = bot.get_file(file_id)
  file.download(FILE_PATH)

  # Чтение файла
  with open(FILE_PATH, "r", encoding='utf-8') as f:
    text = f.read()

  # Поиск номеров телефонов и почты
  phones = re.findall(phone_regex, text)
  emails = re.findall(email_regex, text)


  # Формирование ответа
  response = "Найденные данные:\n\n"
  if phones:
    response += "**Номера телефонов:**\n" + "\n".join(map(str, phones)) + "\n\n"
  if emails:
    response += "**Email адреса:**\n" + "\n".join(map(str, emails))

  # Отправка ответа
  if response != "Найденные данные:\n\n":
    bot.send_message(chat_id=update.message.chat_id, text=response)
  else:
    bot.send_message(chat_id=update.message.chat_id, text="В файле не найдены номера телефонов или email адреса.")

def main():
  """Запускает бота."""
  updater = Updater(BOT_TOKEN)
  dispatcher = updater.dispatcher

  # Обработчик команды /start
  dispatcher.add_handler(CommandHandler("start", start))

  dispatcher.add_handler(CommandHandler("get_emails", get_emails))
  dispatcher.add_handler(CommandHandler("get_phone_numbers", get_phone_numbers))

  # Обработчик входящих файлов
  dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

  dispatcher.add_handler(ConversationHandler(
      entry_points=[CommandHandler('find_email', find_email)],
      states={
          FIND_EMAIL: [MessageHandler(Filters.text & ~Filters.command, find_email_handler)]
      },
      fallbacks=[]
  ))

  dispatcher.add_handler(ConversationHandler(
      entry_points=[CommandHandler('find_phone_number', find_phone_number)],
      states={
          FIND_PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, find_phone_number_handler)]
      },
      fallbacks=[]
  ))

  dispatcher.add_handler(ConversationHandler(
      entry_points=[CommandHandler('verify_password', verify_password_handler)],
      states={
          VERIFY_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, verify_password)]
      },
      fallbacks=[]
  ))

  dispatcher.add_handler(ConversationHandler(
      entry_points=[CommandHandler("save_emails", save_emails, pass_user_data=True)],
      states={
          WRITE_EMAILS: [MessageHandler(Filters.text, save_emails_handler, pass_user_data=True)]
      },
      fallbacks=[CommandHandler("start", start)],
  ))

  dispatcher.add_handler(ConversationHandler(
      entry_points=[CommandHandler("save_phone_numbers", save_phone_numbers, pass_user_data=True)],
      states={
          WRITE_PHONE_NUMBERS: [MessageHandler(Filters.text, save_phone_numbers_handler, pass_user_data=True)]
      },
      fallbacks=[CommandHandler("start", start)],
  ))

  # Запуск бота
  updater.start_polling()
  updater.idle()

if __name__ == "__main__":
  main()

import logging
import re
from telegram import Update, Bot
from telegram.ext import (
  Updater,
  CommandHandler,
  MessageHandler,
  Filters,
)

# Настройка логгирования
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота
BOT_TOKEN = "2127491244:AAFLKvfN1grM8aR0gmzRqrShJo7IJHuKAX8" # Замените на ваш токен

# Регулярные выражения для поиска телефонов и почты
phone_regex = r"((?:\+7|8)?[\s-]?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2}))" # Телефон
email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)" # Почта

# Файл с данными
FILE_PATH = "C:/Users/User/Desktop/ReceivedFile.txt" # Замените на путь к вашему файлу

# Инициализация бота
bot = Bot(token=BOT_TOKEN)

def start(update, context):
  """Отправляет приветственное сообщение."""
  bot.send_message(chat_id=update.message.chat_id, text="Привет! Отправьте мне файл с текстом, я найду в нем номера телефонов и почту.")

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

  # Обработчик входящих файлов
  dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

  # Запуск бота
  updater.start_polling()
  updater.idle()

if __name__ == "__main__":
  main()

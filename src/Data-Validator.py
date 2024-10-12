import re

import psycopg2
import requests
from adodbapi.examples.db_table_names import databasename


class Validator:
  def __init__(self, api_key):
    self.api_key = api_key

  def is_valid_phone(self, phone_number):
    """Проверяет телефон на соответствие формату."""
    phone_regex = r"\+?\d{1,3}\s?(?\d{3})?\s?\d{3}\s?\d{4}"
    match = re.match(phone_regex, phone_number)
    return bool(match)

  def is_valid_email(self, email):
    """Проверяет email на соответствие формату."""
    email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    match = re.match(email_regex, email)
    return bool(match)

  def check_phone_existence_from_external_service(self, phone_number):
    """Проверяет существование телефона (используйте API от подходящего сервиса)."""
    # Замените это на реальный API-запрос
    url = f"https://your-phone-api.com/check?phone={phone_number}&api_key={self.api_key}"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      return data.get("exists")
    return False

  def check_email_existence_from_external_service(self, email):
    """Проверяет существование email (используйте API от подходящего сервиса)."""
    # Замените это на реальный API-запрос
    url = f"https://your-email-api.com/check?email={email}&api_key={self.api_key}"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      return data.get("exists")
    return False

  def check_phone_existence_from_db(self, found_phone_numbers, dataBase):
    try:
        conn = psycopg2.connect(
            host = dataBase.host, databasename = dataBase.name, user = dataBase.user, password = dataBase.password
        )
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT phone_number FROM phone_numbers WHERE phone_number LIKE '%{found_phone_numbers}%'"
        )
        phone_numbers = [row[0] for row in cursor.fetchall()]
        conn.close()
        return phone_numbers

    except Exception as e:
        print(f"Error with connection with DataBase: {e}")

  def check_emails_existence_from_db(self, found_emails, dataBase):
      try:
          conn = psycopg2.connect(
              host=dataBase.host, dataBaseName=dataBase.name, user=dataBase.user, password=dataBase.password
          )
          cursor = conn.cursor()
          cursor.execute(
              f"SELECT email FROM emails WHERE email LIKE '%{found_emails}%'"
          )
          emails = [row[0] for row in cursor.fetchall()]
          conn.close()
          return emails

      except Exception as e:
          print(f"Error with connection with DataBase: {e}")



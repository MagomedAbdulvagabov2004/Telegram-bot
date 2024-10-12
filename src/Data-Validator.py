import re
import requests

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

  def check_phone_existence(self, phone_number):
    """Проверяет существование телефона (используйте API от подходящего сервиса)."""
    # Замените это на реальный API-запрос
    url = f"https://your-phone-api.com/check?phone={phone_number}&api_key={self.api_key}"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      return data.get("exists")
    return False

  def check_email_existence(self, email):
    """Проверяет существование email (используйте API от подходящего сервиса)."""
    # Замените это на реальный API-запрос
    url = f"https://your-email-api.com/check?email={email}&api_key={self.api_key}"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      return data.get("exists")
    return False
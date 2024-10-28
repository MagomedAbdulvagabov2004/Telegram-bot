# Deriving the latest base image
FROM python:3.12.5

# Labels as key value pair
LABEL Maintainer = "Abdulvagabov Magomed"

# iNSTALL PIP REQUIREMENTS
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Any working directory can be chosen as per choice like '/' or '/home' etc
WORKDIR /usr/app/src

COPY /src/telegram-bot.py ./

CMD ["python", "./telegram-bot.py"]

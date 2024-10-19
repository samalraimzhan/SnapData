import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токены
TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'
HUGGING_FACE_API_TOKEN = 'HUGGING_FACE_API_TOKEN'

# URL API Hugging Face
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}

# Функция для команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я здесь, чтобы помочь вам. Если у вас есть какие-либо вопросы или нужна помощь, не стесняйтесь спрашивать! Что я могу сделать для вас сегодня?')

# Функция для взаимодействия с API Hugging Face
def query_hugging_face(prompt):
    data = {"inputs": prompt}
    response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=data)
    return response.json()

# Обработка текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    response_data = query_hugging_face(user_input)
    response_text = response_data[0]['generated_text']
    update.message.reply_text(response_text)

def main():
    # Инициализация бота
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    # Обработка команды /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Обработка текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()

    # Ожидание завершения работы
    updater.idle()

if __name__ == '__main__':
    main()

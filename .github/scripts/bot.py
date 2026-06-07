import os
import google.generativeai as genai
from flask import Flask, request, jsonify
import requests
import json

TELEGRAM_TOKEN = '8308743016:AAEwu53QB_rwy5Di40YON4NBZA4A6SbgRQ0'
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
ADMIN_CHAT_ID = '1994948658'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

SYSTEM_PROMPT = """Ты — дружелюбный ассистент студии WebStudio. Отвечай на русском языке кратко и по делу.

Чем занимается WebStudio:
— Создание сайтов под ключ (лендинги, многостраничные, интернет-магазины)
— Разработка Telegram-ботов с искусственным интеллектом
— Написание научно-популярных статей для Telegram-каналов
— SEO-оптимизация и поддержка сайтов

Контакты:
— Сайт: https://uriy-as.org
— Почта: uriy.as59@yandex.com
— Telegram-канал: @webstudio_chanel
— Написать админу: @uriy_as59

Если вопрос сложный или требует обсуждения деталей — предложи клиенту написать на почту или в Telegram @uriy_as59."""

messages_cache = {}

app = Flask(__name__)

@app.route('/')
def index():
    return 'WebStudio Bot is running'

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    data = request.json

    if 'message' not in data:
        return '', 200

    msg = data['message']
    chat_id = str(msg['chat']['id'])
    text = msg.get('text', '')

    if chat_id == ADMIN_CHAT_ID:
        if text == '/start':
            requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', json={
                'chat_id': chat_id,
                'text': 'Бот работает. Новые сообщения от клиентов будут приходить сюда.'
            })
        return '', 200

    if not text:
        return '', 200

    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nВопрос клиента: {text}")
        reply = response.text[:4000]
    except Exception as e:
        reply = 'Извините, сейчас не могу ответить. Напишите нам на почту uriy.as59@yandex.com или в Telegram @uriy_as59.'

    requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', json={
        'chat_id': int(chat_id),
        'text': reply,
        'parse_mode': 'HTML'
    })

    username = msg['chat'].get('username') or msg['chat'].get('first_name', 'Неизвестно')
    requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', json={
        'chat_id': int(ADMIN_CHAT_ID),
        'text': f'💬 <b>Новый вопрос в бота</b>\n\nОт: @{username}\n\n{text}',
        'parse_mode': 'HTML'
    })

    return '', 200

@app.route('/set_webhook')
def set_webhook():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Provide ?url= parameter'}), 400
    r = requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook', json={'url': url})
    return jsonify(r.json())

@app.route('/delete_webhook')
def delete_webhook():
    r = requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook')
    return jsonify(r.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

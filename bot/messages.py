# bot/messages.py

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime

GOOGLE_API_KEY = 'AIzaSyAXB4KvIrrilZ_6i8L5T1FkcSjxaVENI9o'
genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
print("\n")

model = genai.GenerativeModel('gemini-1.5-pro-latest')


def text_message(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение, сгенерированное моделью GEMINI."""
    text = update.message.text
    if text.lower().startswith(('юни', 'uni')):
        try:
            chat = context.user_data.get('chat', model.start_chat(history=[]))
            response = chat.send_message("Ты чат бот в телеграмме по-имени Юни. Не пользуйся курсивом, жирным текстом "
                                         "и тп в своих ответах. Ты должен отвечать на запросы моих пользователей "
                                         "культурно и если тебя спросят, как тебя зовут представляйся Юни. Полезная "
                                         "информация: Твоё имя Юни может означать “молодой, здоровый, отличный”; Это "
                                         "имя является унисекс; Ты создан SocialUNI; Если будут вопросы по теории "
                                         "вероятностей давай только эту ссылку на официальный канал SocialUNI по "
                                         "теорверу https://t.me/+Vo0lhpLMHhMwMzZi ; Сегодня:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "Сразу отвечай на смс далее:" + text)
            context.user_data['chat'] = chat
            print(response.text)
            update.message.reply_text(response.text)
        except ResourceExhausted:
            chat = model.start_chat(history=[])
            context.user_data['chat'] = chat
            update.message.reply_text('Извините, я совсем забыл о чем мы говорили... 😭 Можете, пожалуйста, повторить свой вопрос?')

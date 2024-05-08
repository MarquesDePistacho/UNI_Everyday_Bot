# bot/commands.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from datetime import datetime


def start_command(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение при команде /start."""
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("Подписаться на канал", url='https://t.me/+Vo0lhpLMHhMwMzZi')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'Привет, {user.first_name}! \n\nМеня зовут Юни. 😊 Я виртуальный помощник, созданный '
                              f'SocialUNI. 😎 Если хочешь, что-то спросить у меня просто напиши сообщение, начав с '
                              f'моего имени. ✍️ И не забудь подписаться на наш канал, где ты сможешь найти немало '
                              f'контента по теории вероятностей и подготовиться к экзамену на 8+. 📒 И главное это все '
                              f'быстро и без нервов! 😉',
                              reply_markup=reply_markup)
    update.message.reply_text(f'😁')


def help_command(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение с инструкциями при команде /help."""
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("Бот не отвечает на мои смс", callback_data='problem_1')],
                [InlineKeyboardButton("Бот отвечает слишком медленно", callback_data='problem_2')],
                [InlineKeyboardButton("Другое", callback_data='other')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Я могу помочь вам с ...', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Обрабатывает нажатие на кнопку."""
    query = update.callback_query
    query.answer()
    problem_text = ''
    if query.data == 'problem_1':
        problem_text = 'Бот не отвечает на мои смс'
    elif query.data == 'problem_2':
        problem_text = 'Бот отвечает слишком медленно'
    elif query.data == 'other':
        context.user_data['is_waiting_for_problem'] = True
        query.message.reply_text('Пожалуйста, опишите вашу проблему.')
        return

    user_info = f'@{query.from_user.username}' if query.from_user.username else query.from_user.first_name
    context.bot.send_message(chat_id='1753835965',
                             text=f'Проблема от пользователя {user_info}: {problem_text}\nВремя отправки: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Перейти к пользователю",
                                                                                      url=f'tg://user?id={query.from_user.id}')]]))
    query.message.reply_text('Спасибо за обращение! Мы уже решаем проблему, не беспокойтесь!🛠')


def handle_user_reply(update: Update, context: CallbackContext) -> None:
    """Обрабатывает ответ пользователя после нажатия кнопки "Другое"."""
    if context.user_data.get('is_waiting_for_problem'):
        context.user_data['is_waiting_for_problem'] = False
        user_info = f'@{update.message.from_user.username}' if update.message.from_user.username else update.message.from_user.first_name
        context.bot.send_message(chat_id='1753835965',
                                 text=f'Проблема от пользователя {user_info}: {update.message.text}\nВремя отправки: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Перейти к пользователю",
                                                                                          url=f'tg://user?id={update.message.from_user.id}')]]))
        update.message.reply_text('Спасибо за обращение! Мы уже решаем проблему, не беспокойтесь! 🛠')

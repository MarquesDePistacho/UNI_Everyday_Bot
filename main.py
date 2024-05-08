# main.py

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from config import TOKEN
from bot.commands import start_command, help_command, handle_user_reply, button
from bot.messages import text_message


def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_user_reply))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

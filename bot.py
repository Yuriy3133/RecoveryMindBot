from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Привет! Бот работает через Updater!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    print("🤖 Бот запущен через Updater...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

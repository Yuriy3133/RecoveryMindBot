import logging
import json
import os
from datetime import datetime, date
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔑 ТВОЙ ТОКЕН — уже вставлен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 📂 Файл для хранения прогресса
PROGRESS_FILE = "progress.json"

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# === Хранение прогресса ===

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"days": []}

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

def days_this_week(days):
    today = date.today()
    week_num = today.isocalendar()[1]
    return sum(1 for day in days if datetime.strptime(day, "%Y-%m-%d").date().isocalendar()[1] == week_num)

# === Кнопки меню ===

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📋 Чек-лист", callback_data="checklist")],
        [InlineKeyboardButton("💊 Добавки", callback_data="supplements")],
        [InlineKeyboardButton("✅ Отметить день", callback_data="track")],
        [InlineKeyboardButton("🔄 Сбросить счётчик", callback_data="reset")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
    ]
    return InlineKeyboardMarkup(keyboard)

# === Команды ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я твой Recovery Bot.\nВыбери, что нужно 👇",
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = load_progress()

    if query.data == "checklist":
        text = (
            "📋 Чек-лист на 30 дней:\n"
            "1–7 день: вода, сон, магний\n"
            "8–14 день: тирозин, адаптогены\n"
            "15–30 день: спорт, дневник"
        )
    elif query.data == "supplements":
        text = (
            "💊 Таблица добавок:\n"
            "Магний — 200–400 мг\n"
            "Витамины B — утром\n"
            "Омега-3 — 1000 мг"
        )
    elif query.data == "track":
        today = date.today().isoformat()
        if today in data["days"]:
            text = "✅ Ты уже отметил этот день! Молодец!"
        else:
            data["days"].append(today)
            save_progress(data)
            text = "✅ День отмечен! Ты на шаг ближе к своей лучшей версии 💪"
    elif query.data == "reset":
        data["days"] = []
        save_progress(data)
        text = "🔄 Счётчик сброшен! Начинаем заново — ты справишься!"
    elif query.data == "stats":
        week_count = days_this_week(data["days"])
        total = len(data["days"])
        text = (
            f"📊 Статистика:\n"
            f"Всего дней отмечено: {total}\n"
            f"На этой неделе: {week_count} дней\n"
            f"Ты красавчик, продолжай! 💪"
        )
    else:
        text = "Неизвестная команда."

    await query.edit_message_text(text, reply_markup=main_menu())

# === Запуск ===

def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()

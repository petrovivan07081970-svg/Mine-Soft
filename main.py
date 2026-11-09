import os
import random
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

MENU = ReplyKeyboardMarkup(
    [["🚀 Получить пример"], ["👤 Мой профиль"], ["ℹ️ О боте"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n\n"
        "Это демонстрационный бот для учебной симуляции.\n"
        "Значения случайные и не предсказывают исход игры. "
        "Не используй их для ставок или денежных решений.",
        reply_markup=MENU
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "🚀 Получить пример":
        value = random.randint(101, 200) / 100
        await update.message.reply_text(
            f"ДЕМО-ПРИМЕР\n\n🚀 {value:.2f}\n\n"
            "Случайное учебное значение. Это не сигнал и не прогноз."
        )
    elif text == "👤 Мой профиль":
        await update.message.reply_text(
            f"Профиль\nИмя: {user.first_name}\n"
            f"Telegram ID: {user.id}\nСтатус: тестовый пользователь"
        )
    elif text == "ℹ️ О боте":
        await update.message.reply_text(
            "Бот показывает случайные демонстрационные значения. "
            "Он не подключён к игровой платформе и не проверяет "
            "платежи, ставки или игровые результаты."
        )
    else:
        await update.message.reply_text("Выбери действие кнопкой ниже.", reply_markup=MENU)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or ADMIN_ID == 0:
        await update.message.reply_text("Команда доступна только администратору.")
        return
    await update.message.reply_text("Бот запущен. Режим: демонстрационный.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()

import logging
import random
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8116470352:AAFFlDQpqqDad5ZHYvsG6px0pWBPNmnB9l4"
GROUP_ID = -1002513778734

greetings = {
    "uz": ["Salom!", "Assalomu alaykum!", "Yaxshi kunlar!", "Salom hammaga!"],
    "ru": ["Привет!", "Здравствуйте!", "Добрый день!", "Всем привет!"],
    "tr": ["Merhaba!", "Selam!", "Günaydın!", "Herkese selam!"]
}

motivations = [
    "Bugun zo‘r kun bo‘ladi!",
    "Sen bunga qodirsan!",
    "Hech qachon taslim bo‘lma!",
    "Harakat – muvaffaqiyat kaliti.",
    "Ishon – hammasi yaxshi bo‘ladi!"
]

def detect_language(text):
    text = text.lower()
    if any(word in text for word in ["salom", "qandaysiz", "ha", "yo'q"]):
        return "uz"
    elif any(word in text for word in ["привет", "здравствуйте", "как дела"]):
        return "ru"
    elif any(word in text for word in ["merhaba", "nasılsın", "günaydın"]):
        return "tr"
    else:
        return "uz"

async def send_hourly_greetings(app):
    lang = random.choice(["uz", "ru", "tr"])
    text = random.choice(greetings[lang])
    await app.bot.send_message(chat_id=GROUP_ID, text=text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = detect_language(update.message.text)
    msg = {
        "uz": "Salom! Men AsianChat botman.",
        "ru": "Привет! Я бот AsianChat.",
        "tr": "Merhaba! Ben AsianChat botuyum."
    }
    await update.message.reply_text(msg[lang])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Boshlash\n/motivate - Ilhom\n/quote - Sitata\n/help - Yordam")

async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(motivations))

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "“Ilm – kuch.” – Francis Bacon",
        "“Orzularingizga yeting!”",
        "“Harakat qilgan – yutadi.”"
    ]
    await update.message.reply_text(random.choice(quotes))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = detect_language(update.message.text)
    reply = {
        "uz": "Men sizni tushundim!",
        "ru": "Я вас понял!",
        "tr": "Sizi anladım!"
    }
    await update.message.reply_text(reply[lang])

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("motivate", motivate))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Hourly greetings uchun scheduler qo‘shamiz
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_hourly_greetings, 'cron', minute=0, args=[app])
    scheduler.start()

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

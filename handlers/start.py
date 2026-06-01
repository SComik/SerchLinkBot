from telegram import Update
from telegram.ext import ContextTypes

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Это бот проверяющий вредоносные ссылки. '
                                    'Скинь свою ссылку и он проверит')
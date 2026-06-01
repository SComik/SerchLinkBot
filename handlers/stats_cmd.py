from telegram import Update
from telegram.ext import ContextTypes
from stats import get_stats

async def stats_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = await get_stats()
    await update.message.reply_text(f'Сегодня проверено ссылок: {count}')
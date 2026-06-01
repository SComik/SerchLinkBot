import asyncio
from datetime import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from stats import load_stats, save_stats

async def load_stats_on_start():
    global stats_today, stats_date
    from stats import stats_today as st_today, stats_date as st_date
    stats_today = await load_stats()
    stats_date = datetime.now().strftime('%Y-%m-%d')
    
    today = datetime.now().strftime('%Y-%m-%d')
    if stats_date != today:
        stats_today = 0
        stats_date = today
        await save_stats(stats_today)

asyncio.run(load_stats_on_start())

application = Application.builder().token(TOKEN).build()

from handlers.start import start_bot
from handlers.stats_cmd import stats_bot
from handlers.message import event_message

application.add_handler(CommandHandler('start', start_bot))
application.add_handler(CommandHandler('stats', stats_bot))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, event_message))

application.run_polling()
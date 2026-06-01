import aiofiles 
from datetime import datetime 

stats_file = "stats.txt"
stats_today = 0
stats_date = datetime.now().strftime('%Y-%m-%d')

async def load_stats():
    try:
        async with aiofiles.open(stats_file, 'r') as f:
            content = await f.read()
            return int(content.strip()) if content.strip() else 0
    except:
        return 0
    
async def save_stats(count):
    async with aiofiles.open(stats_file, 'w') as f:
        await f.write(str(count))



async def update_stats():
    global stats_today, stats_date
    today = datetime.now().strftime('%Y-%m-%d')
    
    if stats_date != today:
        stats_today = 0
        stats_date = today
    
    stats_today += 1
 
    await save_stats(stats_today)

async def get_stats() -> int:
    global stats_today, stats_date
    today = datetime.now().strftime('%Y-%m-%d')
    if stats_date != today:
        return 0
    return stats_today
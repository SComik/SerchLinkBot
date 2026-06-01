import re
from telegram import Update, MessageEntity
from telegram.ext import ContextTypes
from config import VIRUSTOTAL_KEY, WARNING_THRESHOLD, MIN_DOMAIN_LENGTH
from stats import update_stats, get_stats
from api.virustotal import check_url

domain_pattern = r'\b[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?\.[a-zA-Z]{2,}(?:/[^\s]*)?\b'

async def event_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    stats_today = await get_stats()
    remaining = 500 - stats_today
    if remaining <= 0:
        await update.message.reply_text('Лимит VirusTotal на сегодня исчерпан! Попробуйте завтра.')
        return
    
    if remaining <= WARNING_THRESHOLD:
        await update.message.reply_text(f'Внимание! Осталось всего {remaining} проверок на сегодня')

    if not message or not message.text:
        return

    all_urls = []

    # Собираем URL из entities
    if message.entities:
        for entity in message.entities:
            if entity.type == MessageEntity.URL:
                url = message.text[entity.offset:entity.offset + entity.length]
                all_urls.append(url)  
                await update.message.reply_text(f'Обнаружена URL ссылка: {url}')

            elif entity.type == MessageEntity.TEXT_LINK:
                url = entity.url
                all_urls.append(url)
                await update.message.reply_text(f'Обнаружена текстовая ссылка: {url}')

    # Собираем домены без протокола
    domain_matches = re.finditer(domain_pattern, message.text, re.IGNORECASE)
    for match in domain_matches:
        domain = match.group()
        already_found = False
        for existing_url in all_urls:
            if domain in existing_url:
                already_found = True
                break
        if not already_found and len(domain) > MIN_DOMAIN_LENGTH:
            all_urls.append(domain)
            await update.message.reply_text(f'Обнаружен домен без протокола: {domain}')

    if all_urls and VIRUSTOTAL_KEY:
        await update.message.reply_text(f'Проверяю {len(all_urls)} ссылку(и)...')

        for url in all_urls:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            result = await check_url(url, VIRUSTOTAL_KEY)

            await update_stats()

            if result['status'] == 'dangerous':

                await update.message.reply_text(f' Ссылка не безопасна, во избежание случайных нажатий она была удалена. Просим быть аккуратнее')
                await message.delete()
                return
            else:
                await update.message.reply_text(f'Результат для: {url}\n{result["message"]}')

    elif all_urls and not VIRUSTOTAL_KEY:
        await update.message.reply_text('API ключ VirusTotal не настроен. Проверка невозможна.')
# 🔍 Бот для проверки ссылок (VirusTotal)

**Telegram-бот, который проверяет ссылки на вредоносность через VirusTotal API.**

---

## 📌 Что умеет бот

- Распознаёт ссылки в сообщениях (URL, TEXT_LINK, домены без протокола)
- Проверяет их через VirusTotal API
- Показывает вердикт: «Опасно», «Подозрительно», «Безопасно»
- Ведёт статистику проверок за сегодня (сохраняется в файл)
- Сообщает, когда заканчивается дневной лимит VirusTotal
- Предупреждает, если осталось мало проверок
- Удаляет сообщение с опасной ссылкой

---

## 🛠️ Технологии

- **Python 3.13**
- `python-telegram-bot` (v20.x, асинхронный)
- `aiohttp` – асинхронные запросы к API
- `aiofiles` – асинхронная работа с файлами
- **VirusTotal API v3**

---

## 🚀 Как запустить

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/SComik/SerchLinkBot.git
   cd SerchLinkBot
Установи зависимости:

```bash
  pip install -r requirements.txt
```
Создай файл .env и добавь токены 

- TELEGRAM_TOKEN=токен_твоего_бота
- VIRUSTOTAL_API_KEY=твой_ключ_virustotal

Запусти бота:
```bash
python main.py
```
##  Пример работы 
<img width="389" height="574" alt="image" src="https://github.com/user-attachments/assets/0ba99458-6ae0-4d05-b22c-8e1dcac40072" />


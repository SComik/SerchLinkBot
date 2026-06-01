import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
VIRUSTOTAL_KEY = os.getenv('VIRUSTOTAL_API_KEY')

WARNING_THRESHOLD = 10
MIN_DOMAIN_LENGTH = 4
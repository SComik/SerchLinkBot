import base64
import aiohttp
import asyncio
from urllib.parse import urlparse

async def check_url(url: str, api_key: str) -> dict:
    if url.startswith(('http://', 'https://')):
        parsed = urlparse(url)
        url_for_encoding = f"{parsed.netloc}{parsed.path}"
        if parsed.query:
            url_for_encoding += f"?{parsed.query}"
    else:
        url_for_encoding = url

    url_id = base64.urlsafe_b64encode(url_for_encoding.encode()).decode().strip('=')

    api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"

    headers = {
        'x-apikey': api_key
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)

                    if malicious > 0:
                        return {
                            'status': 'dangerous',
                            'message': f'ОПАСНО! Обнаружено {malicious} вредоносных ресурсов',
                            'stats': stats  
                        }
                    elif suspicious > 0:
                        return {
                            'status': 'suspicious',
                            'message': f'ПОДОЗРИТЕЛЬНО! Обнаружено {suspicious} подозрительных ресурсов',
                            'stats': stats  
                        }
                    else:
                        return {
                            'status': 'safe',
                            'message': 'БЕЗОПАСНО! Ссылка не обнаружена в базах вредоносных ресурсов',
                            'stats': stats  
                        }
                elif response.status == 404:
                    return {
                        'status': 'safe',
                        'message': 'URL не найден в базе (вероятно, безопасен)',
                        'stats': {}
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f'Ошибка API VirusTotal: {response.status}',
                        'stats': {}
                    }
        except asyncio.TimeoutError:  
            return {
                'status': 'error',
                'message': 'Таймаут при проверке ссылки. Попробуйте позже.',
                'stats': {}
            }
        except aiohttp.ClientError as e:  
            return {
                'status': 'error',
                'message': f'Ошибка соединения: {str(e)}',
                'stats': {}
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Ошибка при проверке: {str(e)}',
                'stats': {}
            }
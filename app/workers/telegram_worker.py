import os
import requests
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
class TelegramWorker:
    async def send_message(self,chat_id,message):
        url = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN)
        params = {"chat_id": chat_id,
                  "text": message,
                  "parse_mode": "Markdown"
                  }
        try:
            response = requests.post(url,params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(e)


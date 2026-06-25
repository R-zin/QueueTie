import os
from email_worker import EmailWorker
from celery import Celery
from telegram_worker import TelegramWorker
REDIS_URL = os.environ.get("REDIS_URL")

app = Celery("celery_app",broker=REDIS_URL,backend=REDIS_URL)

@app.task
async def send_email(to,subject,body):
    try:
        c = EmailWorker()
        await c.send_email(to,subject,body)
    except Exception as e:
        raise Exception(e)
@app.task
async def send_sms(to,subject,body):
    try:
        await TelegramWorker.send_message(to,subject,body)
    except Exception as e:
        raise Exception(e)





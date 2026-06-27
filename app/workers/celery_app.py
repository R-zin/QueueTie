import os

from celery.app import autoretry
import asyncio
from email_worker import EmailWorker
from celery import Celery
from telegram_worker import TelegramWorker
REDIS_URL = os.environ.get("REDIS_URL")

app = Celery("celery_app",broker=REDIS_URL,backend=REDIS_URL)

@app.task(bind=True,autoretry_for=(Exception,),retry_backoff=True,max_retries=5)
def send_email(to,subject,body):
    try:
        c = EmailWorker()
        asyncio.run(c.send_email(to,subject,body))
    except Exception as e:
        raise Exception(e)
@app.task
def send_sms(to,subject,body):
    try:
        asyncio.run(TelegramWorker.send_message(to,subject,body))
    except Exception as e:
        raise Exception(e)





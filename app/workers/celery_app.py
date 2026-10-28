import asyncio
import os

from celery import Celery

try:
    from app.workers.email_worker import EmailWorker
    from app.workers.telegram_worker import TelegramWorker
except ImportError:
    from .email_worker import EmailWorker
    from .telegram_worker import TelegramWorker

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

app = Celery("celery_app", broker=REDIS_URL, backend=REDIS_URL)


@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def send_email(self, to, subject, body):
    try:
        c = EmailWorker()
        asyncio.run(c.send_email(to, subject, body))
    except Exception as e:
        raise Exception(e)


@app.task
def send_sms(to, subject, body):
    try:
        message = f"{subject}\n{body}" if subject else body
        asyncio.run(TelegramWorker.send_message(to, message))
    except Exception as e:
        raise Exception(e)

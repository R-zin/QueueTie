import os
from email_worker import EmailWorker
from celery import Celery

REDIS_URL = os.environ.get("REDIS_URL")

app = Celery("celery_app",broker=REDIS_URL,backend=REDIS_URL)

@app.task
async def send_email(to,subject,body):
    try:
        c = EmailWorker()
        await c.send_email(to,subject,body)
    except Exception as e:
        raise Exception(e)



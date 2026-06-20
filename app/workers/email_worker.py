import os
import aiosmtplib
from email.message import EmailMessage


class EmailWorker():
    async def send_email(self,to:str,subject:str,body:str):
        message = EmailMessage()
        message["From"] = os.getenv("SMTP_FROM")
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)
        await aiosmtplib.send(message,hostname=os.getenv("SMTP_HOSTNAME"),
                              port=os.getenv("SMTP_PORT"),
                              username=os.getenv("SMTP_USERNAME"),
                              password=os.getenv("SMTP_PASSWORD"),
                              start_tls=True)
    async def process(self,job:dict):
        payload = job["Payload"]
        try:
            await self.send_email(to=payload["to"], subject=payload["subject"], body=payload["body"])
            return {
                "status":"Successful",
                "worker":"EmailWorker"
            }
        except ValueError as e:
            return {
                "status":"Failed",
                "message":f"{str(e)}",
                "worker":"EmailWorker"
            }



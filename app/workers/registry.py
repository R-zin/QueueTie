from .email_worker import EmailWorker
from .telegram_worker import TelegramWorker

REGISTRY = {
    "email_worker":EmailWorker
    "telegram_notification":TelegramWorker
}
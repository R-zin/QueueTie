try:
    from app.workers.email_worker import EmailWorker
    from app.workers.telegram_worker import TelegramWorker
except ImportError:
    from .email_worker import EmailWorker
    from .telegram_worker import TelegramWorker

REGISTRY = {
    "email_worker": EmailWorker,
    "telegram_notification": TelegramWorker,
}

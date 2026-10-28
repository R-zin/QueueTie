from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def test_registry_contains_workers():
    from app.workers.registry import REGISTRY

    assert "email_worker" in REGISTRY
    assert "telegram_notification" in REGISTRY


@pytest.mark.anyio
async def test_telegram_worker_send_message():
    from app.workers.telegram_worker import TelegramWorker

    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        res = await TelegramWorker.send_message("123456", "Test message")
        assert res == {"ok": True}


def test_celery_send_sms_task():
    from app.workers.celery_app import send_sms

    with patch(
        "app.workers.telegram_worker.TelegramWorker.send_message", new_callable=AsyncMock
    ) as mock_send:
        mock_send.return_value = {"ok": True}
        send_sms("123456", "Alert", "Server is down")
        mock_send.assert_called_once_with("123456", "Alert\nServer is down")


def test_celery_send_email_task():
    from app.workers.celery_app import send_email

    with patch(
        "app.workers.email_worker.EmailWorker.send_email", new_callable=AsyncMock
    ) as mock_send_email:
        mock_send_email.return_value = None
        # send_email is bound, so calling the underlying function directly or task
        send_email.apply(args=["test@example.com", "Subject", "Body"])
        mock_send_email.assert_called_once_with("test@example.com", "Subject", "Body")

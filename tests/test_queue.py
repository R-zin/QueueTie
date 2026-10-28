from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.routes.Queue import ADMIN_KEY

client = TestClient(app)


def test_list_queues():
    with patch("app.routes.Queue.r") as mock_redis:
        mock_redis.scan_iter.return_value = ["emails", "sms"]
        mock_redis.llen.side_effect = lambda k: 5 if k == "emails" else 2

        response = client.get("/queues")
        assert response.status_code == 200
        data = response.json()
        assert "queues" in data
        assert data["queues"] == [{"name": "emails", "size": 5}, {"name": "sms", "size": 2}]


def test_get_queue_stats():
    with patch("app.routes.Queue.r") as mock_redis:
        mock_redis.lrange.return_value = ['{"type": "email"}', '{"type": "sms"}']

        response = client.get("/queues/emails")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 2


def test_purge_queue_without_admin_key_fails():
    response = client.delete("/queues/emails")
    assert response.status_code == 422  # Missing header


def test_purge_queue_with_invalid_admin_key_fails():
    response = client.delete("/queues/emails", headers={"x-admin-key": "wrong_key"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Admin key is invalid"


def test_purge_queue_success():
    with patch("app.routes.Queue.r") as mock_redis:
        mock_redis.unlink.return_value = 1

        response = client.delete("/queues/emails", headers={"x-admin-key": ADMIN_KEY})
        assert response.status_code == 200
        assert response.json() == {"Status": "Successfully purged"}
        mock_redis.unlink.assert_called_once_with("emails")

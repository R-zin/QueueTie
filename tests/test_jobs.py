from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.dbmodel import Job, JobStatus
from app.routes.job import get_db
from app.workers.database import Base

# Setup test SQLite in-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_job_persists_to_db(client, db_session):
    """Test creating a job persists to DB and returns job details."""
    payload = {
        "queue": "emails",
        "type": "send_email",
        "Payload": {"to": "test@example.com", "subject": "Welcome", "body": "Hello"},
    }
    with patch("app.routes.job.enqueue", new_callable=AsyncMock) as mock_enqueue:
        response = client.post("/jobs", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "created_time" in data
        assert data["msg"] == "Job Successfully created"

        # Verify job was persisted to the database
        job_id = data["id"]
        job_in_db = db_session.query(Job).filter(Job.id == job_id).first()
        assert job_in_db is not None
        assert job_in_db.job_status == JobStatus.RUNNING
        assert job_in_db.time_start is not None
        assert job_in_db.time_end is None

        # Verify enqueue was called
        mock_enqueue.assert_called_once()
        call_args = mock_enqueue.call_args[0]
        assert call_args[0] == "emails"
        assert call_args[1]["type"] == "send_email"
        assert call_args[1]["Payload"] == payload["Payload"]


def test_list_jobs_empty(client):
    """Test listing jobs when none exist returns empty list."""
    response = client.get("/jobs")
    assert response.status_code == 200
    assert response.json() == []


def test_list_jobs_with_entries(client, db_session):
    """Test listing jobs returns all existing jobs with correct attributes."""
    job1 = Job(id="job-1", time_start=datetime(2026, 1, 1, 10, 0), job_status=JobStatus.RUNNING)
    job2 = Job(id="job-2", time_start=datetime(2026, 1, 1, 11, 0), job_status=JobStatus.SUCCESS)
    db_session.add_all([job1, job2])
    db_session.commit()

    response = client.get("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    ids = [j["id"] for j in data]
    assert "job-1" in ids
    assert "job-2" in ids


def test_get_job_status_existing(client, db_session):
    """Test fetching an existing job by ID returns its details."""
    job = Job(id="job-123", time_start=datetime(2026, 1, 1, 12, 0), job_status=JobStatus.RUNNING)
    db_session.add(job)
    db_session.commit()

    response = client.get("/jobs/job-123")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "job-123"
    assert data["job_status"] == "RUNNING"


def test_get_job_status_not_found(client):
    """Test fetching a non-existent job returns 404."""
    response = client.get("/jobs/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_delete_job_existing(client, db_session):
    """Test deleting an existing job removes it from the database."""
    job = Job(id="job-delete-me", time_start=datetime.utcnow(), job_status=JobStatus.RUNNING)
    db_session.add(job)
    db_session.commit()

    response = client.delete("/jobs/job-delete-me")
    assert response.status_code == 200
    assert response.json() == {"status": "Job successfully deleted"}

    deleted_job = db_session.query(Job).filter(Job.id == "job-delete-me").first()
    assert deleted_job is None


def test_delete_job_not_found(client):
    """Test deleting a non-existent job returns 404."""
    response = client.delete("/jobs/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"

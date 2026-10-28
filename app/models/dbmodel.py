import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, String

try:
    from app.workers.database import Base
except ImportError:
    from workers.database import Base


class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True)
    time_start = Column(DateTime, default=datetime.utcnow)
    time_end = Column(DateTime, nullable=True)
    job_status = Column(Enum(JobStatus, name="job_status"), default=JobStatus.RUNNING)

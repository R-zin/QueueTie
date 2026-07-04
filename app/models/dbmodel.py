from workers.database import Base
from sqlalchemy import Column, Integer, String,DateTime,Enum
from uuid import uuid4
import enum

class JobStatus(str,enum.Enum):
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True)
    time_start = Column(DateTime)
    time_end = Column(DateTime,nullable=True)
    job_status = Column(Enum(JobStatus, name="job_status"))




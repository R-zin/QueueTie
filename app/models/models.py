from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Create_Job_Input(BaseModel):
    queue: str
    type: str
    Payload: Any


create_Job_In = Create_Job_Input


class create_job_Response(BaseModel):
    id: str
    created_time: datetime = Field(default_factory=datetime.utcnow)
    msg: str


class list_queue_out(BaseModel):
    name: str
    size: int

from pydantic import BaseModel
from typing import Any
from datetime import datetime
class create_Job_In(BaseModel):
    type:str
    priority:int
    payload: Any

class create_job_Response(BaseModel):
    id:str
    created_time:datetime
    msg:str

class list_queue_out(BaseModel):
    name:str
    size:int

from pydantic import BaseModel
from typing import Any
from datetime import datetime

class Create_Job_Input(BaseModel):
    queue:str
    type:str
    Payload:Any



class create_job_Response(BaseModel):
    id:str
    created_time:datetime
    msg:str

class list_queue_out(BaseModel):
    name:str
    size:int

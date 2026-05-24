from pydantic import BaseModel
from typing import Any
class create_Job_In(BaseModel):
    type:str
    priority:int
    payload: Any


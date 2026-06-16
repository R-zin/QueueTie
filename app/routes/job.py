
from fastapi import APIRouter,HTTPException
from uuid import uuid4
from ..models.models import create_Job_In,create_job_Response,Create_Job_Input
from app.Broker.producer import enqueue

router = APIRouter()

@router.get("/jobs")
async def list_jobs():
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.post("/jobs",response_model=create_job_Response)
async def create_job(data:Create_Job_Input):
    try:
        packet = {
            "type":data.type,
            "Payload":data.Payload
        }
        await enqueue(data.queue,packet)
        res = create_job_Response(id=str(uuid4()),msg="Job Successfully created")
        return res
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@router.get('/jobs/{id}')
async def get_job_status(id:str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.delete("/jobs/{id}")
async def delete(id:str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

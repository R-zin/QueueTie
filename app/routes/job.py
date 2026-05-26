from fastapi import APIRouter,HTTPException
from uuid import uuid4
from ..models.models import create_Job_In,create_job_Response

router = APIRouter()

@router.get("/jobs")
async def list_jobs():
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.post("/jobs",response_model=create_job_Response)
async def create_job(data:create_Job_In):
    try:

        res = create_job_Response(id=str(uuid4()),msg="Job Successfully created")
        return res
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@router.get('/jobs/{id}')
async def get_job_status(id:str):
    try:
        pass
    except Exception as e:
        raise HTTPException()

@router.delete("/jobs/{id}")
async def delete(id:str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

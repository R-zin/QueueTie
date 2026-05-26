
from fastapi import APIRouter,HTTPException
from .. models.models import list_queue_out
router = APIRouter()

@router.get("/queues",response_model=list_queue_out)
async def list_queues():
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.get("/queues/{queue_name}")
async def get_stats_queue(queue_name:str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.delete("/queues/{queue_name}")
async def purge(queue_name:str):  #Make this admin only
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))



import redis
from fastapi import APIRouter,HTTPException
from fastapi import Depends,Header
from .. models.models import list_queue_out
import os

ADMIN_KEY = os.environ['ADMIN_KEY']

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
router = APIRouter()

def admin_route(x_admin_key:str = Header(...)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401,detail="Admin key is invalid")
    return True


@router.get("/queues",response_model=list_queue_out)
async def list_queues():
    try:
        res = []
        for key in r.scan_iter(_type="LIST"):
            res.append({key:r.llen(key)})
        return {"queues":res}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.get("/queues/{queue_name}") #Fetching the tasks pending in Queue
async def get_stats_queue(queue_name:str):
    try:
        res = r.lrange(queue_name, 0, -1)
        return {"items":res}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.delete("/queues/{queue_name}",dependencies=[Depends(admin_route)])
async def purge(queue_name:str):  #Make this admin only
    try:
        await r.unlink(queue_name)
        return {"Status":"Successfully purged"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))



import json
from .Redis_client import client



async def enqueue(data:dict,QUEUE):
    await client.lpush(QUEUE,json.dumps(data))
    

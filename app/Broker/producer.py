import json
from .Redis_client import client

QUEUE = "jobs"

async def enqueue(data:dict):
    await client.lpush(QUEUE,json.dumps(data))
    

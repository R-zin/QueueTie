import json
from .Redis_client import client

QUEUE = "jobs"

async def consume_job():
    job = await client.brpop(QUEUE)
    if not job:
        return None
    _,payload = job
    return json.loads(payload)



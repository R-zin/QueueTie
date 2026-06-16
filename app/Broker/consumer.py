import json
from .Redis_client import client


async def consume_job(QUEUE):
    job = await client.brpop(QUEUE)
    if not job:
        return None
    _,payload = job
    return json.loads(payload)



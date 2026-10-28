import json

try:
    from app.workers.Redis_client import client
except ImportError:
    from workers.Redis_client import client


async def enqueue(queue: str, data: dict):
    if client is not None:
        await client.lpush(queue, json.dumps(data))

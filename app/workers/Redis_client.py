import os

import redis.asyncio as redis

redis_host = os.getenv("REDIS_CLIENT", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

try:
    client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
except Exception:
    client = None

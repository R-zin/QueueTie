import redis.asyncio as redis
import os
client = redis.Redis(host=os.getenv("REDIS_CLIENT"),
                     port=int(os.getenv("REDIS_PORT")),
                     decode_responses=True)




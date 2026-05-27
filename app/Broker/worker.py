import asyncio
from ..workers.worker_runner import WorkerRunner
from .consumer import consume_job

runner = WorkerRunner()

async def worker_loop():
    while True:
        try:
            job = await consume_job()
            res = runner.execute(job)
        except Exception as e:
            print("Worker error")
            asyncio.sleep(1)
if __name__ == "__main__":
    asyncio.run(worker_loop())



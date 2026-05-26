from registry import REGISTRY

class WorkerRunner:
    def __int__(self):
        pass
    async def execute(self,job:dict):
        job_type = job["type"]
        worker = REGISTRY.get(job_type)
        if not worker:
            raise Exception("No worker found")
        res = await  worker.process(job)
        return res



from fastapi import FastAPI
from routes.job import router as job_router
from routes.Queue import router as queue_router
app = FastAPI(title="QueueTie",version="1.0.0")

app.include_router(job_router)
app.include_router(queue_router)

@app.get("/health")
async def health_check():
    try:
        return {"status": "ok"}
    except:
        return {"status": "error"}



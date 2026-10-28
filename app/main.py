from fastapi import FastAPI

try:
    from app.routes.job import router as job_router
    from app.routes.Queue import router as queue_router
except ImportError:
    from routes.job import router as job_router
    from routes.Queue import router as queue_router

app = FastAPI(title="QueueTie", version="1.0.0")

app.include_router(job_router)
app.include_router(queue_router)


@app.get("/health")
async def health_check():
    try:
        return {"status": "ok"}
    except Exception:
        return {"status": "error"}

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from app.Broker.producer import enqueue
    from app.models.dbmodel import Job, JobStatus
    from app.models.models import Create_Job_Input, create_job_Response
    from app.workers.database import SessionLocal
except ImportError:
    from Broker.producer import enqueue
    from models.dbmodel import Job, JobStatus
    from models.models import Create_Job_Input, create_job_Response
    from workers.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/jobs")
async def list_jobs(db: Session = Depends(get_db)):
    try:
        jobs = db.query(Job).all()
        return [
            {
                "id": j.id,
                "time_start": j.time_start.isoformat() if j.time_start else None,
                "time_end": j.time_end.isoformat() if j.time_end else None,
                "job_status": j.job_status.value
                if hasattr(j.job_status, "value")
                else str(j.job_status),
            }
            for j in jobs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jobs", response_model=create_job_Response)
async def create_job(data: Create_Job_Input, db: Session = Depends(get_db)):
    try:
        now = datetime.utcnow()
        p_db = Job(id=str(uuid4()), time_start=now, time_end=None, job_status=JobStatus.RUNNING)
        packet = {"id": p_db.id, "type": data.type, "Payload": data.Payload}
        await enqueue(data.queue, packet)
        db.add(p_db)
        db.commit()
        db.refresh(p_db)
        return create_job_Response(
            id=p_db.id, created_time=p_db.time_start, msg="Job Successfully created"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{id}")
async def get_job_status(id: str, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.id == id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return {
            "id": job.id,
            "time_start": job.time_start.isoformat() if job.time_start else None,
            "time_end": job.time_end.isoformat() if job.time_end else None,
            "job_status": job.job_status.value
            if hasattr(job.job_status, "value")
            else str(job.job_status),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/jobs/{id}")
async def delete(id: str, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.id == id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        db.delete(job)
        db.commit()
        return {"status": "Job successfully deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter,HTTPException


router = APIRouter()

@router.post("/jobs")
async def create_job(data:)
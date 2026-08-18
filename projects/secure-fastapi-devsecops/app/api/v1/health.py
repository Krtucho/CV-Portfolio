from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@router.get("/ready")
async def readiness():
    return {"status": "ready"}


@router.get("/live")
async def liveness():
    return {"status": "alive"}

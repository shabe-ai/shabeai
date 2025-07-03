from fastapi import APIRouter, status

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    """
    Placeholder endpoint so the module exists.
    Lets us extend with streaming chat in step 0-5+.
    """
    return {"status": "ok"}

from fastapi import APIRouter, Depends

from ..database import get_session
from ..deps import get_current_active_user
from ..schemas.deal import DealCreate, DealOut
from ..services.deal_service import DealService

router = APIRouter(prefix="/deals", tags=["deals"])

@router.get("/", response_model=list[DealOut])
def list_deals(db=None, _=None):
    if db is None:
        db = Depends(get_session)
    if _ is None:
        _ = Depends(get_current_active_user)
    return DealService(db).list()

@router.post("/", response_model=DealOut, status_code=201)
def create_deal(deal: DealCreate, db=None, _=None):
    if db is None:
        db = Depends(get_session)
    if _ is None:
        _ = Depends(get_current_active_user)
    return DealService(db).create(deal) 
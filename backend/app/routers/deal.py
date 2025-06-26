from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..services.deal_service import DealService
from ..schemas.deal import DealCreate, DealOut
from ..deps import get_current_active_user

router = APIRouter(prefix="/deals", tags=["deals"])

@router.get("/", response_model=list[DealOut])
def list_deals(db: Session = Depends(get_session), _=Depends(get_current_active_user)):
    return DealService(db).list()

@router.post("/", response_model=DealOut, status_code=201)
def create_deal(deal: DealCreate, db: Session = Depends(get_session), _=Depends(get_current_active_user)):
    return DealService(db).create(deal) 
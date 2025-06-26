from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..services.lead_service import LeadService
from ..schemas.lead import LeadCreate, LeadOut

router = APIRouter(prefix="/leads", tags=["leads"])

@router.get("/", response_model=list[LeadOut])
def list_leads(db: Session = Depends(get_session)):
    return LeadService(db).list()

@router.post("/", response_model=LeadOut, status_code=201)
def create_lead(lead: LeadCreate, db: Session = Depends(get_session)):
    return LeadService(db).create(lead) 
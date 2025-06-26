from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..services.company_service import CompanyService
from ..schemas.company import CompanyCreate, CompanyOut
from ..deps import get_current_active_user

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("/", response_model=list[CompanyOut])
def list_companies(db: Session = Depends(get_session), _=Depends(get_current_active_user)):
    return CompanyService(db).list()

@router.post("/", response_model=CompanyOut, status_code=201)
def create_company(company: CompanyCreate, db: Session = Depends(get_session), _=Depends(get_current_active_user)):
    return CompanyService(db).create(company) 
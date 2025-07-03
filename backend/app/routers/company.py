from fastapi import APIRouter, Depends

from ..database import get_session
from ..schemas.company import CompanyCreate, CompanyOut
from ..services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=list[CompanyOut])
def list_companies(db=None):
    if db is None:
        db = Depends(get_session)
    return CompanyService(db).list()


@router.post("/", response_model=CompanyOut, status_code=201)
def create_company(company: CompanyCreate, db=None):
    if db is None:
        db = Depends(get_session)
    return CompanyService(db).create(company)

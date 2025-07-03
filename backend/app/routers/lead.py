import structlog
from fastapi import APIRouter, Depends, Request

from ..database import get_session
from ..schemas.lead import LeadCreate, LeadOut
from ..services.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("/", response_model=list[LeadOut])
def list_leads(request: Request, db=Depends(get_session)):
    log = structlog.get_logger().bind(
        component="leads-api", request_id=request.state.request_id
    )
    log.info("leads_list_requested")
    leads = LeadService(db).list()
    log.info("leads_list_retrieved", count=len(leads))
    return leads


@router.post("/", response_model=LeadOut, status_code=201)
def create_lead(lead: LeadCreate, request: Request, db=Depends(get_session)):
    log = structlog.get_logger().bind(
        component="leads-api", request_id=request.state.request_id
    )
    log.info("lead_creation_requested", lead_email=lead.email)
    new_lead = LeadService(db).create(lead)
    log.info("lead_created", lead_id=new_lead.id)
    return new_lead

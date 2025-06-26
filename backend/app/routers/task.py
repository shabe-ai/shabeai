from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..services.task_service import TaskService
from ..schemas.task import TaskCreate, TaskOut
from ..deps import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_session), _=Depends(get_current_active_user)):
    return TaskService(db).list()

@router.post("/", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_session), _=Depends(get_current_active_user)):
    return TaskService(db).create(task) 
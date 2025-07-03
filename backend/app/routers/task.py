from fastapi import APIRouter, Depends

from ..database import get_session
from ..deps import get_current_active_user
from ..schemas.task import TaskCreate, TaskOut
from ..services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskOut])
def list_tasks(db=None, _=None):
    if db is None:
        db = Depends(get_session)
    if _ is None:
        _ = Depends(get_current_active_user)
    return TaskService(db).list()

@router.post("/", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db=None, _=None):
    if db is None:
        db = Depends(get_session)
    if _ is None:
        _ = Depends(get_current_active_user)
    return TaskService(db).create(task) 
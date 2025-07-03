from fastapi import APIRouter, Depends

from ..database import get_session
from ..schemas.task import TaskCreate, TaskOut
from ..services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskOut])
def list_tasks(db=Depends(get_session)):
    return TaskService(db).list()


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db=Depends(get_session)):
    return TaskService(db).create(task)

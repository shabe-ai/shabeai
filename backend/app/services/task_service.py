from sqlmodel import Session, select

from ..models import Task


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def list(self):
        return self.session.exec(select(Task)).all()

    def get(self, task_id: str):
        return self.session.get(Task, task_id)

    def create(self, task_in):
        task = Task(**task_in.model_dump())
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, db_task, task_update):
        for k, v in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, k, v)
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def delete(self, db_task):
        self.session.delete(db_task)
        self.session.commit() 
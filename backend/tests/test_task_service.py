import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from app.services.task_service import TaskService
from app.models import Task, Lead


def test_task_service_list_tasks(session):
    """Test listing tasks through the service"""
    # Create a lead first
    lead = Lead(firstName="Test", lastName="Lead", email="testlead_list@example.com")
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    # Create some tasks
    due_date = datetime.now() + timedelta(days=7)
    tasks = [
        Task(title="Task 1", dueDate=due_date, isDone=False, leadId=lead.id),
        Task(title="Task 2", dueDate=due_date, isDone=True, leadId=lead.id)
    ]
    for task in tasks:
        session.add(task)
    session.commit()
    
    service = TaskService(session)
    all_tasks = service.list()
    assert len(all_tasks) >= 2
    titles = [task.title for task in all_tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles


def test_task_service_get_task(session):
    """Test getting a task by ID through the service"""
    # Create a lead first
    lead = Lead(firstName="Test", lastName="Lead 2", email="testlead_get@example.com")
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    # Create a task
    due_date = datetime.now() + timedelta(days=5)
    task = Task(title="Test Task", dueDate=due_date, isDone=False, leadId=lead.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    
    service = TaskService(session)
    retrieved_task = service.get(task.id)
    assert retrieved_task.id == task.id
    assert retrieved_task.title == "Test Task"


def test_task_service_get_task_not_found(session):
    """Test getting a task that doesn't exist"""
    service = TaskService(session)
    result = service.get("non-existent-id")
    assert result is None


def test_task_service_create_task(session):
    """Test creating a task through the service"""
    # Create a lead first
    lead = Lead(firstName="Test", lastName="Lead 3", email="testlead_create@example.com")
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    service = TaskService(session)
    due_date = datetime.now() + timedelta(days=10)
    task_data = {
        "title": "New Task",
        "dueDate": due_date,
        "isDone": False,
        "leadId": lead.id
    }
    
    task = service.create(task_data)
    assert task.title == "New Task"
    assert task.leadId == lead.id
    assert task.isDone is False
    assert task.id is not None


def test_task_service_update_task(session):
    """Test updating a task through the service"""
    # Create a lead first
    lead = Lead(firstName="Test", lastName="Lead 4", email="testlead_update@example.com")
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    # Create a task
    due_date = datetime.now() + timedelta(days=3)
    task = Task(title="Original Task", dueDate=due_date, isDone=False, leadId=lead.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    
    service = TaskService(session)
    new_due_date = datetime.now() + timedelta(days=15)
    update_data = {"title": "Updated Task", "dueDate": new_due_date, "isDone": True}
    
    updated_task = service.update(task, update_data)
    assert updated_task.title == "Updated Task"
    assert updated_task.isDone is True


def test_task_service_delete_task(session):
    """Test deleting a task through the service"""
    # Create a lead first
    lead = Lead(firstName="Test", lastName="Lead 5", email="testlead_delete@example.com")
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    # Create a task
    due_date = datetime.now() + timedelta(days=1)
    task = Task(title="Delete Me", dueDate=due_date, isDone=False, leadId=lead.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    
    service = TaskService(session)
    service.delete(task)
    
    # Verify it's deleted
    result = service.get(task.id)
    assert result is None 
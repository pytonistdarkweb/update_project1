import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from app.services.task_services import TaskService
from app.domain.value_objects.time_interval import TimeInterval
from app.domain.essence.schemas.task import TaskCreate, TaskRead

@pytest.mark.asyncio
async def test_create_task():
    
    mock_task_repo = AsyncMock()
    mock_task_read_repo = AsyncMock()
    mock_task_repo.create_task.return_value = TaskCreate(
        task_id=1,
        title="Test Task",
        description="This is a test task",
        start_time=datetime(2023, 10, 1, 10, 0, 0),
        end_time=datetime(2023, 10, 1, 11, 0, 0)
    )

    
    task_service = TaskService(task_repo=mock_task_repo, task_read_repo=mock_task_read_repo)

    
    created_task = await task_service.create_task(
        user_id=1,
        title="Test Task",
        description="This is a test task",
        start_time=datetime(2023, 10, 1, 10, 0, 0),
        end_time=datetime(2023, 10, 1, 11, 0, 0)
    )

    
    assert created_task.title == "Test Task"
    assert created_task.description == "This is a test task"
    assert created_task.start_time == datetime(2023, 10, 1, 10, 0, 0)
    assert created_task.end_time == datetime(2023, 10, 1, 11, 0, 0)
    mock_task_repo.create_task.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_tasks():
    
    mock_task_repo = AsyncMock()
    mock_task_read_repo = AsyncMock()
    mock_task_read_repo.get_tasks_by_user.return_value = [
        TaskRead(
            id=1,
            user_id=1,
            title="Test Task",
            description="This is a test task",
            start_time=datetime(2023, 10, 1, 10, 0, 0),
            end_time=datetime(2023, 10, 1, 11, 0, 0)
        )
    ]

    
    task_service = TaskService(task_repo=mock_task_repo, task_read_repo=mock_task_read_repo)

    
    tasks = await task_service.get_tasks(user_id=1)

    
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    mock_task_read_repo.get_tasks_by_user.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_update_task():
    
    mock_task_repo = AsyncMock()
    mock_task_read_repo = AsyncMock()
    mock_task_repo.update_task.return_value = TaskRead(
        task_id=1,
        title="Updated Task",
        description="This is an updated task",
        start_time=datetime(2023, 10, 1, 10, 0, 0),
        end_time=datetime(2023, 10, 1, 11, 0, 0)
    )

    
    task_service = TaskService(task_repo=mock_task_repo, task_read_repo=mock_task_read_repo)

    
    updated_task = await task_service.update_task(task_id=1, title="Updated Task")

    
    assert updated_task.title == "Updated Task"
    mock_task_repo.update_task.assert_awaited_once_with(1, title="Updated Task")

@pytest.mark.asyncio
async def test_delete_task():
    
    mock_task_repo = AsyncMock()
    mock_task_read_repo = AsyncMock()
    mock_task_repo.delete_task.return_value = None

    
    task_service = TaskService(task_repo=mock_task_repo, task_read_repo=mock_task_read_repo)

    
    result = await task_service.delete_task(task_id=1)

    
    assert result is None
    mock_task_repo.delete_task.assert_awaited_once_with(1)

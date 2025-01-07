import pytest
from app.infrastructure.repository.task_write_repo import TaskWriteRepository
from app.infrastructure.repository.user_repo import UserWriteRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.essence.models.task import Task
from app.domain.essence.models.user import User
from datetime import datetime, timedelta
import uuid


@pytest.mark.asyncio
async def test_create_task(main_db_session: AsyncSession):
    
    user_repo = UserWriteRepository(main_db_session)
    await user_repo.create_user(
        username="testuser",
        email="test@example.com",
        password_hash="hashedpassword"
    )

    
    task_repo = TaskWriteRepository(main_db_session)
    unique_title = f"Task {uuid.uuid4()}"
    task = Task(
        user_id=1,
        title=unique_title,
        description="This is a test task",
        start_time=datetime(2025, 1, 1, 10, 0),
        end_time=datetime(2025, 1, 1, 11, 0),
    )
    created_task = await task_repo.create_task(task)

    assert created_task.title == unique_title
    assert created_task.description == "This is a test task"
    assert created_task.user_id == 1
    assert created_task.start_time < created_task.end_time


@pytest.mark.asyncio
async def test_update_task(main_db_session: AsyncSession):
    
    user_repo = UserWriteRepository(main_db_session)
    created_user = await user_repo.create_user(
        username="testuser",
        email="test@example.com",
        password_hash="hashedpassword"
    )
    await main_db_session.refresh(created_user)

    
    task_repo = TaskWriteRepository(main_db_session)
    task = Task(
        user_id=created_user.id,
        title="Initial Task",
        description="Initial description",
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
    )
    main_db_session.add(task)
    await main_db_session.commit()
    await main_db_session.refresh(task)

    
    updated_title = "Updated Task"
    updated_task = await task_repo.update_task(
        task_id=task.id,
        title=updated_title,
        description="This is an updated test task"
    )

    
    assert updated_task.title == updated_title
    assert updated_task.description == "This is an updated test task"

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.essence.models.task import Task
from app.infrastructure.repository.task_read_repo import TaskReadRepository
from app.infrastructure.repository.task_write_repo import TaskWriteRepository
from app.infrastructure.repository.user_repo import UserWriteRepository
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_get_tasks_by_user(main_db_session: AsyncSession):
    
    user_repo = UserWriteRepository(main_db_session)
    created_user = await user_repo.create_user(
        username="testuser",
        email="testuser@example.com",
        password_hash="hashedpassword"
    )
    await main_db_session.refresh(created_user)

    
    current_time = datetime.now()
    task = Task(
        user_id=created_user.id,
        title="Test Task",
        description="Task description",
        start_time=current_time,
        end_time=current_time + timedelta(hours=1),
    )
    main_db_session.add(task)
    await main_db_session.commit()
    await main_db_session.refresh(task)


    read_repo = TaskReadRepository(main_db_session)
    tasks = await read_repo.get_tasks_by_user(user_id=created_user.id)

    
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].description == "Task description"
    assert tasks[0].user_id == created_user.id
    assert tasks[0].start_time == current_time 
    assert tasks[0].end_time == current_time + timedelta(hours=1) 

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.essence.models.task import Task
from app.infrastructure.repository.task_read_repo import TaskReadRepository
from app.infrastructure.repository.user_repo import UserWriteRepository
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_get_task_by_id(main_db_session: AsyncSession):
    
    user_repo = UserWriteRepository(main_db_session)
    created_user = await user_repo.create_user(
        username="testuser",
        email="testuser@example.com",
        password_hash="hashedpassword"
    )
    await main_db_session.refresh(created_user)

    current_time = datetime.now()
    task = Task(
        user_id=created_user.id,
        title="Test Task",
        description="Task description",
        start_time=current_time,
        end_time=current_time + timedelta(hours=1),
    )
    main_db_session.add(task)
    await main_db_session.commit()
    await main_db_session.refresh(task)

    read_repo = TaskReadRepository(main_db_session)

    
    result = await read_repo.get_task_by_id(task_id=task.id)

    
    assert result is not None
    assert result.id == task.id
    assert result.title == "Test Task"
    assert result.description == "Task description"
    assert result.user_id == created_user.id
    assert result.start_time == current_time
    assert result.end_time == current_time + timedelta(hours=1)





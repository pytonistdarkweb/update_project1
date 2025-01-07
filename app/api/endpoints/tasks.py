from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List
from app.domain.essence.schemas.task import TaskCreate, TaskUpdate
from app.services.task_services import TaskService
from app.domain.essence.schemas.user import User
from app.infrastructure.dependency import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.domain.essence.schemas.task import TaskRead, TaskUpdate, TaskDelete
from app.api.except_endpoints import TaskNotFoundError, UnauthorizedUserError



tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.post("", response_model=TaskCreate, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task_service = TaskService(session)
    try:
        return await task_service.create_task(task_data, current_user)
    except UnauthorizedUserError as e:
        UnauthorizedUserError.raise_unauthorized_user_error()


@tasks_router.get("/{all}", response_model=List[TaskRead])
async def get_tasks(session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task_service = TaskService(session)
    return await task_service.get_tasks(current_user.id)


@tasks_router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskUpdate, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task_service = TaskService(session)
    try:
        return await task_service.update_task(task_id, task_data, current_user)
    except TaskNotFoundError as e:
        TaskNotFoundError.raise_task_not_found_error(task_id)
    except UnauthorizedUserError as e:
        UnauthorizedUserError.raise_unauthorized_user_error()


@tasks_router.delete("/{task_id}", response_model=TaskDelete)
async def delete_task(task_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task_service = TaskService(session)
    try:
        return await task_service.delete_task(task_id, current_user)
    except TaskNotFoundError as e:
        TaskNotFoundError.raise_task_not_found_error(task_id)
    except UnauthorizedUserError as e:
        UnauthorizedUserError.raise_unauthorized_user_error()


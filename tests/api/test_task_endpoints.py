import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.domain.essence.schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskDelete
from app.domain.essence.schemas.user import User
from app.services.task_services import TaskService
from app.api.except_endpoints import TaskNotFoundError, UnauthorizedUserError
from unittest.mock import AsyncMock, MagicMock,patch
import httpx
from app.services.token_creation_service import TokenService
from tests.conftest import generate_valid_token,test_user


@pytest.mark.asyncio
async def test_create_task(task_data: dict, test_user, async_client: httpx.AsyncClient):
    mock_task_service = AsyncMock()
    mock_task_service.create_task.return_value = TaskCreate(**task_data)
    valid_token = generate_valid_token()
    with patch('app.services.task_services', return_value=mock_task_service), \
        patch('app.api.deps.get_current_user', return_value=test_user):
        response = await async_client.post(
            "/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {valid_token}"}
        )
    assert response.status_code == 201
    assert response.json()["title"] == "New Task"
    assert response.json()["description"] == "Task description"
    mock_task_service.create_task.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_tasks(client, mock_task_service, mock_user):
    task_data = [TaskRead(id=1, title="Test Task", description="Test Description", time_slot="2025-01-01T12:00:00")]
    mock_task_service.get_tasks = MagicMock(return_value=task_data)
    response = await client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {mock_user.id}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Task"


@pytest.mark.asyncio
async def test_update_task(client, mock_task_service, mock_user):
    task_id = 1
    task_data = TaskUpdate(title="Updated Task", description="Updated Description", time_slot="2025-01-01T14:00:00")
    mock_task_service.update_task = MagicMock(return_value=TaskRead(id=task_id, **task_data.model_dump()))
    
    response = await client.put(
        f"/tasks/{task_id}",
        json=task_data.model_dump(),
        headers={"Authorization": f"Bearer {mock_user.id}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Task"
    assert response.json()["description"] == "Updated Description"


@pytest.mark.asyncio
async def test_delete_task(client, mock_task_service, mock_user):
    task_id = 1
    task_delete = TaskDelete(id=task_id, status="Deleted")
    mock_task_service.delete_task = MagicMock(return_value=task_delete)
    
    response = await client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {mock_user.id}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "Deleted"
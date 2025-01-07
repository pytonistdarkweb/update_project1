from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.domain.essence.models.task import Task
from app.infrastructure.repository.task_user_repo_session import TaskUserRepository


class TaskReadRepository(TaskUserRepository):

    async def get_tasks_by_user(self, user_id: int) -> list[Task]:
        query = select(Task).where(Task.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        result = await self.session.execute(
            select(Task).where(Task.id == task_id))
        return result.scalars().first()
    
    
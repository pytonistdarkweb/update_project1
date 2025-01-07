from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.essence.models.task import Task
from typing import Optional
from app.infrastructure.repository.task_user_repo_session import TaskUserRepository


class TaskWriteRepository(TaskUserRepository):

    async def create_task(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task


    async def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        task = await self.session.get(Task, task_id)
        if not task:
            return None
        for key, value in kwargs.items():
            setattr(task, key, value)
        await self.session.commit()
        await self.session.refresh(task)
        return task


    async def delete_task(self, task_id: int) -> bool:
        task = await self.session.get(Task, task_id)
        if task:
            await self.session.delete(task)
            await self.session.commit()
            return True
        return False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
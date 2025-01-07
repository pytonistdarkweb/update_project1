from app.infrastructure.repository.task_read_repo import TaskReadRepository
from app.infrastructure.repository.task_write_repo import TaskWriteRepository
from app.domain.essence.models.task import Task
from app.domain.value_objects.time_interval import TimeInterval
from typing import List, Optional




class TaskService:
    def __init__(self, task_repo: TaskWriteRepository, task_read_repo: TaskReadRepository):
        self.task_repo = task_repo
        self.task_read_repo = task_read_repo

    async def create_task(
        self, 
        user_id: int, 
        title: str, 
        description: str, 
        start_time: str, 
        end_time: str,
    ) -> Task:
        
        
        time_interval = TimeInterval(start_time=start_time, end_time=end_time)
        time_interval.validate()
    
    
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        created_task = await self.task_repo.create_task(task)
        return created_task

    async def get_tasks(
        self, 
        user_id: int, 
    ) -> List[Task]:
        tasks = await self.task_read_repo.get_tasks_by_user(user_id)
        return tasks

    async def update_task(
        self, 
        task_id: int, 
        **kwargs
    ) -> Optional[Task]:
        updated_task = await self.task_repo.update_task(task_id, **kwargs)
        return updated_task

    async def delete_task(self, task_id: int) -> bool:
        return await self.task_repo.delete_task(task_id)
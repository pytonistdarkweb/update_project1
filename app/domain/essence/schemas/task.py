from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Task(BaseModel):
    task_id: int = Field(None, gt=0)
    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    start_time: datetime
    end_time: datetime


class TaskRead(Task):
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime


class TaskUpdate(Task):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class TaskDelete(Task):
    pass
    


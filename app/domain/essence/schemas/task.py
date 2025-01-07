from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class Task(BaseModel):
    class Config(ConfigDict):
        model_config = ConfigDict(orm_mode=True)


class TaskCreate(Task):
    title: str = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    start_time: datetime
    end_time: datetime


class TaskRead(Task):
    task_id: int = Field(None, gt=0)
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime


class TaskUpdate(Task):
    task_id: int = Field(None, gt=0)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class TaskDelete(Task):
    task_id: int = Field(None, gt=0)
    pass
    


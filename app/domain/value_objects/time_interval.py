from datetime import datetime
from pydantic import BaseModel

class TimeInterval(BaseModel):
    start_time: datetime
    end_time: datetime

    def validate(self):
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be earlier than end_time")
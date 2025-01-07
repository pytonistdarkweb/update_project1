from sqlalchemy.ext.asyncio import AsyncSession


class TaskUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
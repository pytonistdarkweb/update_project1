from operator import and_
from typing import Optional
from app.domain.essence.models.user import User
from app.infrastructure.repository.task_user_repo_session import TaskUserRepository
from sqlalchemy.future import select


class UserWriteRepository(TaskUserRepository):


    async def create_user(self, username: str, email: str, password_hash: str) -> User:
        user = User(
            username=username, 
            email=email, 
            password_hash=password_hash
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def get_user(self, email: str, username: str, password_hash: str) -> Optional[User]:
        query = select(User).where(and_(User.email == email, User.username == username, User.password_hash == password_hash))
        result = await self.session.execute(query) 
        return result.scalar_one_or_none()



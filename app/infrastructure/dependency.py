from app.infrastructure.db import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:    
            await session.close()
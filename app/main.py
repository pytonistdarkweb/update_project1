from fastapi import FastAPI
from app.infrastructure.resources import close_db
from app.api.endpoints.auth import auth_router
from app.api.endpoints.tasks import tasks_router
from contextlib import asynccontextmanager
import uvicorn
from app.core.config import server_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Initialize resources if needed.")
    try:
        yield
    finally:
        print("Application shutdown: Closing database connections.")
        await close_db()


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(tasks_router)


if __name__ == "__main__":
    uvicorn.run(
        "app/main:app", 
        host=server_settings.HOST,
        port=server_settings.PORT,
        reload=server_settings.RELOAD
)
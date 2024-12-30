from fastapi import FastAPI
import uvicorn
from app.core.config import server_settings,ServerSettings
from app.infrastructure.db import close_db
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Initialize resources if needed.")
    try:
        yield
    finally:
        print("Application shutdown: Closing database connections.")
        await close_db()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}




if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=server_settings.HOST,
        port=server_settings.PORT,
        reload=server_settings.RELOAD
)
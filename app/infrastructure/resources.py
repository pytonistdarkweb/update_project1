import logging
from app.infrastructure.db import engine


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def close_db():
    try:
        logger.info("Closing database connections...")
        await engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error closing database: {e}")
        raise
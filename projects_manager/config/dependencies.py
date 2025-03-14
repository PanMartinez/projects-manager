from projects_manager.config.db import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

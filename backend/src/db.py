import os
import logging
from typing import AsyncGenerator
from dotenv import load_dotenv

# 1. Import AsyncSession ONLY from SQLModel to avoid confusion
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://todo_user:todo_password@localhost/todo_db")

# For NeonDB compatibility (Fixing SSL for asyncpg)
if "neon.tech" in DATABASE_URL:
    if "?ssl=require" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("?ssl=require", "")
    # Note: asyncpg handles SSL automatically for NeonDB

# 2. FIXED: Use the 'DATABASE_URL' variable, not 'settings.DATABASE_URL'
engine = create_async_engine(
    DATABASE_URL,
    echo=True,            # Log SQL queries (Great for debugging)
    future=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)

# 3. FIXED: Explicitly use the SQLModel AsyncSession class
AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession, 
    expire_on_commit=False
)

async def create_db_and_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        try:
            await conn.run_sync(SQLModel.metadata.create_all)
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")
            raise

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async sessions"""
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logging.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()
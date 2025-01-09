import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_SERVER")}/{os.getenv("POSTGRES_DB")}', echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=True, autocommit=False, autoflush=False)

os.getenv("TOKEN")

class Base(AsyncAttrs, DeclarativeBase):
    pass

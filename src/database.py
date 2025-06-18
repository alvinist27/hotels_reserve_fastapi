from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.DB_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

# import asyncio
#
# from sqlalchemy import text
# async def fetch_postgresql_version():
#     async with async_session() as session:
#         res = await session.execute(text('SELECT version();'))
#         print(res.fetchone())
#
#
# if __name__ == '__main__':
#     asyncio.run(fetch_postgresql_version())

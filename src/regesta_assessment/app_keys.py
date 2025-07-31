from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

db_session = web.AppKey("db_session", async_sessionmaker[AsyncSession])

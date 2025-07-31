from collections.abc import AsyncGenerator
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typenv import Env

from regesta_assessment import app_keys
from regesta_assessment.routes import routes


def main() -> None:
    async def create_db_session(app: web.Application) -> AsyncGenerator[None]:
        engine = create_async_engine(env.str("DB_URL"))
        app[app_keys.db_session] = async_sessionmaker(engine)
        yield
        await engine.dispose()

    env = Env()
    env.read_env()

    port = env.int("PORT")

    app = web.Application()

    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader("regesta_assessment"))
    app.add_routes(routes)

    app[aiohttp_jinja2.static_root_key] = "/static"
    app.router.add_static("/static", Path(__file__).parent / "static", name="static")

    app.cleanup_ctx.append(create_db_session)

    web.run_app(app, port=port)


if __name__ == "__main__":
    main()

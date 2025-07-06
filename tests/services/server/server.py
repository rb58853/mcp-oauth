from mcp_oauth.server.oauth_server import (
    OAuthServer,
    SimpleAuthSettings,
    AuthServerSettings,
)
from uvicorn import Config, Server
from .api import app, server_settings
import asyncio
import logging
import os

logger = logging.getLogger(__name__)


def run_oauth_server():
    server_settings: AuthServerSettings = AuthServerSettings(
        host="127.0.0.1",
        port=9000,
        server_url="http://127.0.0.1:9000",
        auth_callback_path="http://127.0.0.1:9000/login",
    )

    # You can use just SimpleAuthSettings(). Next is the base configuration
    auth_settings: SimpleAuthSettings = SimpleAuthSettings(
        superusername=os.getenv("SUPERUSERNAME"),
        superuserpassword=os.getenv("SUPERUSERPASSWORD"),
        mcp_scope="user",
    )

    oauth_server: OAuthServer = OAuthServer(
        server_settings=server_settings, auth_settings=auth_settings
    )
    oauth_server.run_starlette_server()


def sample_fastapi_mcp_server():
    async def uvicorn_run():
        config = Config(
            app,
            host=server_settings.host,
            port=server_settings.port,
            log_level="info",
        )
        server = Server(config)
        logger.info(
            f"🚀 MCP Fastapi Server running on http://{server_settings.host}:{server_settings.port}"
        )
        await server.serve()

    asyncio.run(uvicorn_run())
    return app

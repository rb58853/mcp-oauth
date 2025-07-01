from pydantic import BaseModel
from ....src.mcp_oauth.server.oauth_server import OAuthServer
from uvicorn import Config, Server
from mcp_server import mcp, FastMCP, server_settings

import asyncio
import logging

logger = logging.getLogger(__name__)


def run_oauth_server():
    oauth_server: OAuthServer = OAuthServer()
    oauth_server.run_starlette_server()


def sample_fastapi_mcp_server():
    mcp = None
    app = None

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

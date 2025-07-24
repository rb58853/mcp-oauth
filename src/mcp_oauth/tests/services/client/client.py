from mcp.client.session import ClientSession
from mcp.shared.exceptions import McpError
from client.oauth_client import OAuthClient
from .example_servers.server_settings import ServerSettings
from .example_servers.servers import my_example_server, github_mcp_server

import asyncio
from datetime import timedelta
from mcp.client.streamable_http import streamablehttp_client
import os


def sample_mcp_client():
    settings:ServerSettings = my_example_server()

    async def open_session():
        print("📡 Opening StreamableHTTP transport connection with auth...")
        async with streamablehttp_client(
            url=settings.server_url,
            headers=settings.headers,
            auth=settings.oauth,
            timeout=timedelta(seconds=60),
        ) as (read_stream, write_stream, get_session_id):
            print("🤝 Initializing MCP session...")
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✨ Session initialization complete!")

                print(f"\n✅ Connected to MCP server at {settings.server_url}")
                if get_session_id:
                    session_id = get_session_id()
                    if session_id:
                        print(f"Session ID: {session_id}")

                tools = await session.list_tools()

                print("\n⚙️  Aviable Tools")
                for tool in tools.tools:
                    print(f"   • {tool.name}: {tool.description}")

    asyncio.run(open_session())

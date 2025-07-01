from mcp.client.session import ClientSession
from pydantic import AnyHttpUrl
from ....src.mcp_oauth.client.oauth_client import OAuthClient

import asyncio
from datetime import timedelta
from mcp.client.streamable_http import streamablehttp_client


def sample_mcp_client():
    # Es necesario tener un servidor MCP corriendo en la direccion http://127.0.0.1:8000//example-server/mcp por httpstream
    server_url: str = "http://127.0.0.1:8000//example-server/mcp"

    # Es necesario tener un servidor OAuth corriendo en la direccion http://localhost:9000
    oauth_client: OAuthClient = OAuthClient(client_name="sample_client")

    print("📡 Opening StreamableHTTP transport connection with auth...")

    async def open_session():
        async with streamablehttp_client(
            url=server_url,
            auth=oauth_client.oauth,
            timeout=timedelta(seconds=60),
        ) as (read_stream, write_stream, get_session_id):
            print("🤝 Initializing MCP session...")
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✨ Session initialization complete!")

                print(f"\n✅ Connected to MCP server at {server_url}")
                if get_session_id:
                    session_id = get_session_id()
                    if session_id:
                        print(f"Session ID: {session_id}")

    asyncio.run(open_session())

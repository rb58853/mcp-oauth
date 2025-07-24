from mcp_oauth import OAuthClient
from .server_settings import ServerSettings
import os


def my_example_server() -> ServerSettings:
    server_url: str = "http://127.0.0.1:8000/example-server/mcp"
    headers: dict[str, str] | None = None
    body: dict = {
        "username": "user",
        "password": "password",
    }
    oauth_client: OAuthClient | None = OAuthClient(
        client_name="sample_client",
        mcp_server_url=server_url,
        body=body,
    )
    oauth = oauth_client.oauth

    return ServerSettings(
        server_url=server_url,
        headers=headers,
        body=body,
        oauth=oauth,
    )


def github_mcp_server() -> ServerSettings:
    access_token: str = os.environ.get("GITHUB_ACCESS_TOKEN", "your_access_token_here")
    server_url: str = "https://api.githubcopilot.com/mcp/"
    headers = {"Authorization": f"Bearer {access_token}"}

    return ServerSettings(
        server_url=server_url,
        headers=headers,
    )

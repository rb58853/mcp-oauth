from .client_provider.client_provider import (
    SimpleOAuthClientProvider,
    OAuthClientProvider,
)
from mcp.shared.auth import OAuthClientMetadata
from .features.token_storage import FileTokenStorage
from .features.callbacks import CallbackFunctions


# TODO: Dar opcion a otras redirect_uris que no sea el server local
class OAuthClient:
    """MCP client with auth support."""

    def __init__(
        self,
        client_name: str,
        mcp_server_url: str,
        redirect_uris: list[str] = ["http://localhost:3030/callback"],
        redirect_uri_port: int = 3030,
        body: dict | None = None,
    ):
        """
        Initialize the OAuthClient with the necessary parameters.

        :param str client_name: Name of the client.
        :param str mcp_server_url: URL of the MCP server.
        :param list[str] redirect_uris: List of redirect URIs for the OAuth flow.
        :param int redirect_uri_port: Port for the redirect URI (default is 3030).
        :return: None
        """
        self.client_name: str = client_name
        self.redirect_uri_port: int = redirect_uri_port
        self.redirect_uris = redirect_uris

        self.body: dict | None = body

        self.server_url: str = mcp_server_url
        self.token_storage = FileTokenStorage(server_name=self.server_url)

        self.__oauth: SimpleOAuthClientProvider | None = None
        """private class variable"""

    @property
    def oauth(self) -> OAuthClientProvider:
        if self.__oauth is not None:
            return self.__oauth

        try:
            callback_functions: CallbackFunctions = CallbackFunctions(
                port=self.redirect_uri_port,
                body=self.body,
            )
            client_metadata_dict = {
                "client_name": self.client_name,
                "redirect_uris": self.redirect_uris,
                "grant_types": ["authorization_code", "refresh_token"],
                "response_types": ["code"],
                "token_endpoint_auth_method": "client_secret_post",
            }

            self.__oauth = SimpleOAuthClientProvider(
                # self.__oauth = OAuthClientProvider(
                server_url=self.server_url.replace("/mcp", ""),
                client_metadata=OAuthClientMetadata.model_validate(
                    client_metadata_dict
                ),
                storage=self.token_storage,
                redirect_handler=callback_functions._default_redirect_handler,
                callback_handler=callback_functions.callback_handler,
            )
            return self.__oauth
        except:
            return None

    def delete_server_credentials_data(self):
        """Delete credentials (token and client_info) from the current_server"""
        self.token_storage.delete_current_server_credentials_data()

    def __get_oauht_from_mcp_server(self, mcp_server_url: str) -> str:
        """
        Get the OAuth server URL from the MCP server.

        :param str mcp_server_url: URL of the MCP server.
        :return: OAuth server URL.
        """
        import requests

        endpoints: list[str] = [
            ".well-known/oauth-protected-resource",
            ".well-known/oauth-protected-resource/mcp",  # github mcp use case
            ".well-known/oauth-authorization-server",
            ".well-known/openid-configuration",
        ]
        end_removables: list[str] = ["/mcp", "/mcp/"]
        for end in end_removables:
            if mcp_server_url.endswith(end):
                mcp_server_url = mcp_server_url[: -len(end)]

        for endpoint in endpoints:
            response = requests.get(f"{mcp_server_url}/{endpoint}")
            if response.status_code == 200:
                servers: list[str] | None = response.json().get(
                    "authorization_servers", None
                )
                if servers is not None:
                    return servers[0]

        raise ValueError(
            f"Failed to retrieve OAuth server URL from MCP server, need manual oauth server url: {response.status_code}"
        )

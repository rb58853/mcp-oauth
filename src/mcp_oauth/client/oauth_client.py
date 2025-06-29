import asyncio
from mcp.client.auth import OAuthClientProvider
from mcp.shared.auth import OAuthClientMetadata
from .features.token_storage import InMemoryTokenStorage
from .features.callbacks import CallbackFunctions


# TODO: Dar opcion a otras redirect_uris que no sea el server local
class OAuthClient:
    """MCP client with auth support."""

    def __init__(
        self,
        client_name: str,
        server_url: str = "http://localhost:9000",
        # redirect_uris: list[str] = ["http://localhost:3030/callback"],
        redirect_uri_port=3030,
    ):
        self.client_name = client_name
        self.redirect_uri_port = redirect_uri_port
        self.redirect_uris = [f"http://localhost:{redirect_uri_port}/callback"]
        # self.redirect_uris = redirect_uris
        self.server_url = server_url

        self.__oauth: OAuthClientProvider | None = None
        """private class variable"""

    @property
    def oauth(self) -> OAuthClientProvider:
        if self.__oauth is not None:
            return self.__oauth

        try:
            callback_functions: CallbackFunctions = CallbackFunctions(
                self.redirect_uri_port
            )
            client_metadata_dict = {
                "client_name": self.client_name,
                "redirect_uris": self.redirect_uris,
                "grant_types": ["authorization_code", "refresh_token"],
                "response_types": ["code"],
                "token_endpoint_auth_method": "client_secret_post",
            }

            self.__oauth = OAuthClientProvider(
                server_url=self.server_url.replace("/mcp", ""),
                client_metadata=OAuthClientMetadata.model_validate(
                    client_metadata_dict
                ),
                storage=InMemoryTokenStorage(),
                redirect_handler=callback_functions._default_redirect_handler,
                callback_handler=callback_functions.callback_handler,
            )
            return self.__oauth
        except:
            return None

    def register(self):
        async def register_awaited():
            client_metadata: OAuthClientMetadata = OAuthClientMetadata(
                redirect_uris=self.redirect_uris, client_name=self.client_name
            )
            resp = await self.oauth._register_oauth_client(
                server_url=self.server_url,
                client_metadata=client_metadata,
            )
            return resp

        return asyncio.run(register_awaited())

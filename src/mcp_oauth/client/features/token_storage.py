from mcp.client.auth import TokenStorage
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken
import os


class FileTokenStorage(TokenStorage):
    """Simple in-memory token storage implementation."""

    def __init__(self):
        tokens = None

        self._tokens: OAuthToken | None = tokens
        self._client_info: OAuthClientInformationFull | None = None

    async def get_tokens(self) -> OAuthToken | None:
        return self._tokens

    async def set_tokens(self, tokens: OAuthToken) -> None:
        self._tokens = tokens
        criptografy_token: str = Criptografy.generate_oauthtoken(self._tokens)
        pass

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        return self._client_info

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        self._client_info = client_info
        criptografy_token: str = Criptografy.generate_clientinfo(self._client_info)
        pass


CRIPTOGRAFY_KEY = os.getenv("CRIPTOGRAFY-KEY")


class Criptografy:
    def generate_oauthtoken(tokens: OAuthToken) -> str:
        my_json = tokens.model_dump_json()
        jose_token = ""
        return jose_token

    def get_oauthtoken(token: str) -> OAuthToken:
        pass

    def generate_clientinfo(client_info: OAuthClientInformationFull) -> str:
        my_json = client_info.model_dump_json()
        return "1234567890"

    def get_clientinfo(token: str) -> OAuthClientInformationFull:
        pass

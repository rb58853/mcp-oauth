from mcp.client.auth import OAuthClientProvider, TokenStorage, httpx
from collections.abc import AsyncGenerator, Awaitable, Callable
from mcp.shared.auth import OAuthClientMetadata


class SimpleOAuthClientProvider(OAuthClientProvider):
    def __init__(
        self,
        server_url: str,
        client_metadata: OAuthClientMetadata,
        storage: TokenStorage,
        redirect_handler: Callable[[str], Awaitable[None]],
        callback_handler: Callable[[], Awaitable[tuple[str, str | None]]],
        timeout: float = 300.0,
    ):
        """Initialize OAuth2 authentication."""
        super().__init__(
            server_url=server_url,
            client_metadata=client_metadata,
            storage=storage,
            redirect_handler=redirect_handler,
            callback_handler=callback_handler,
            timeout=timeout,
        )

    async def _discover_protected_resource(self) -> httpx.Request:
        return super()._discover_protected_resource()

    async def _handle_protected_resource_response(
        self, response: httpx.Response
    ) -> None:
        return super()._handle_protected_resource_response(response=response)

    def _build_well_known_path(self, pathname: str) -> str:
        return super()._build_well_known_path(pathname=pathname)

    def _should_attempt_fallback(self, response_status: int, pathname: str) -> bool:
        return super()._should_attempt_fallback(
            response_status=response_status, pathname=pathname
        )

    async def _try_metadata_discovery(self, url: str) -> httpx.Request:
        return super()._try_metadata_discovery(url=url)

    async def _discover_oauth_metadata(self) -> httpx.Request:
        return super()._discover_oauth_metadata()

    async def _discover_oauth_metadata_fallback(self) -> httpx.Request:
        return super()._discover_oauth_metadata_fallback()

    async def _handle_oauth_metadata_response(
        self, response: httpx.Response, is_fallback: bool = False
    ) -> bool:
        return super()._handle_oauth_metadata_response(
            response=response, is_fallback=is_fallback
        )

    async def _register_client(self) -> httpx.Request | None:
        return super()._register_client()

    async def _handle_registration_response(self, response: httpx.Response) -> None:
        return super()._handle_registration_response(response=response)

    async def _perform_authorization(self) -> tuple[str, str]:
        return super()._perform_authorization()

    async def _exchange_token(
        self, auth_code: str, code_verifier: str
    ) -> httpx.Request:
        return super()._exchange_token(auth_code=auth_code, code_verifier=code_verifier)

    async def _handle_token_response(self, response: httpx.Response) -> None:
        return super()._handle_token_response(response=response)

    async def _refresh_token(self) -> httpx.Request:
        return super()._refresh_token()

    async def _handle_refresh_response(self, response: httpx.Response) -> bool:
        return super()._handle_refresh_response(response=response)

    async def _initialize(self) -> None:
        return super()._initialize()

    def _add_auth_header(self, request: httpx.Request) -> None:
        return super()._add_auth_header(request)

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        return super().async_auth_flow(request)

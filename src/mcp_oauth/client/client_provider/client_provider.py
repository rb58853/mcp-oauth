from mcp.client.auth import (
    OAuthClientProvider,
    TokenStorage,
    httpx,
    AsyncGenerator,
    Awaitable,
    Callable,
    OAuthClientMetadata,
    MCP_PROTOCOL_VERSION,
    LATEST_PROTOCOL_VERSION,
    urljoin,
    urlparse,
    logger,
    ValidationError,
    OAuthRegistrationError,
    OAuthClientInformationFull,
    re,
)

from ..features.token_storage import FileTokenStorage


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
        self._initialized = False
        self.storage: FileTokenStorage = storage
        """`FileTokenStorage` reference for use class methods"""

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        """HTTPX auth flow integration."""
        async with self.context.lock:
            is_registed_client: bool = False
            while not is_registed_client:
                is_registed_client = True
                if not self._initialized:
                    await self._initialize()

                # Capture protocol version from request headers
                self.context.protocol_version = request.headers.get(
                    MCP_PROTOCOL_VERSION
                )

                if (
                    not self.context.is_token_valid()
                    and self.context.can_refresh_token()
                ):
                    # Try to refresh token
                    refresh_request = await self._refresh_token()
                    refresh_response = yield refresh_request

                    if not await self._handle_refresh_response(refresh_response):
                        # Refresh failed, need full re-authentication
                        self._initialized = False

                if self.context.is_token_valid():
                    self._add_auth_header(request)

                response = yield request

                if response.status_code == 401:
                    # Perform full OAuth flow
                    try:
                        # OAuth flow must be inline due to generator constraints
                        # Step 1: Discover protected resource metadata (RFC9728 with WWW-Authenticate support)
                        discovery_request = await self._discover_protected_resource(
                            response
                        )
                        discovery_response = yield discovery_request
                        await self._handle_protected_resource_response(
                            discovery_response
                        )

                        # Step 2: Discover OAuth metadata (with fallback for legacy servers)
                        discovery_urls = self._get_discovery_urls()
                        for url in discovery_urls:
                            request = self._create_oauth_metadata_request(url)
                            response = yield request

                            if response.status_code == 200:
                                try:
                                    await self._handle_oauth_metadata_response(response)
                                    break
                                except ValidationError:
                                    continue
                            elif response.status_code != 404:
                                break  # Non-404 error, stop trying

                        # Step 3: Register client if needed
                        registration_request = await self._register_client()
                        if registration_request:
                            registration_response = yield registration_request
                            await self._handle_registration_response(
                                registration_response
                            )

                        # Step 4: Perform authorization
                        try:
                            auth_code, code_verifier = (
                                await self._perform_authorization()
                            )
                        except:
                            is_registed_client = False
                            self.storage.delete_current_server_credentials_data()
                            continue

                        # Step 5: Exchange authorization code for tokens
                        token_request = await self._exchange_token(
                            auth_code, code_verifier
                        )
                        token_response = yield token_request
                        await self._handle_token_response(token_response)
                    except Exception:
                        logger.exception("OAuth flow error")
                        raise

        # Retry with new tokens
        self._add_auth_header(request)
        yield request

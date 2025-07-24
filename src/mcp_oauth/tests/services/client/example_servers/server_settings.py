from pydantic import BaseModel, ConfigDict
from mcp.client.auth import OAuthClientProvider


class ServerSettings(BaseModel):
    """
    Settings for the example server used in tests.
    """
    # field: type(any)  # campo con tipo arbitrario
    model_config = ConfigDict(
        arbitrary_types_allowed=True  # Permite tipos arbitrarios sin error
    )
    
    server_url: str | None = None
    headers: dict[str, str] | None = None
    body: dict[str, any] | None = None
    oauth: OAuthClientProvider | None = None

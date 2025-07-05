"""
OAuthProvider server for `"mcp[cli]"` running in RAM Memory for develop time.

`🔔 NOTE: We working on app "for production OAuth"`
"""

# TODO: Remove try
try:
    from client.oauth_client import OAuthClient
    from server.oauth_server import OAuthServer
    from server.token_verifier.token_verifier import IntrospectionTokenVerifier
    from start_env import main as start_env_base

    __all__ = [
        "OAuthClient",
        "OAuthServer",
        "IntrospectionTokenVerifier",
        "start_env_base",
    ]

except Exception as e:
    print(f"WARNING: {e}")

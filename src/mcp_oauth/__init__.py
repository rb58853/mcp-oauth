"""
OAuthProvider server for `"mcp[cli]"` running in RAM Memory for develop time.

`🔔 NOTE: We working on app "for production OAuth"`
"""

# TODO: Remove try
try:
    from client.oauth_client import OAuthClient
    from server.oauth_server import OAuthServer
    from server.token_verifier.token_verifier import IntrospectionTokenVerifier

    __all__ = ["OAuthClient", "OAuthServer", "IntrospectionTokenVerifier"]

except Exception as e:
    print(f"WARNING: {e}")

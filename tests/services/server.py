from ...src.mcp_oauth.server.oauth_server import OAuthServer


def run_oauth_server():
    oauth_server: OAuthServer = OAuthServer()
    oauth_server.run_starlette_server()


def sample_mcp_server():
    pass

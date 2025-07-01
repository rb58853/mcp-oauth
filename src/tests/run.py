from .services.client.client import sample_mcp_client
from .services.server.server import sample_fastapi_mcp_server

def run_client():
    sample_mcp_client()

def run_server():
    sample_fastapi_mcp_server()
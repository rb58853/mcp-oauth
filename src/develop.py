from mcp_oauth.client.oauth_client import SimpleAuthClient


def main():
    client = SimpleAuthClient(client_name="my_client")
    client.register()
    client.oauth


main()

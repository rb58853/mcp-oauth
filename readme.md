# MCP OAuth

<div align = center>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/mcp-oauth?color=%2334D058&label=Version)](https://pypi.org/project/mcp-oauth)
[![Last commit](https://img.shields.io/github/last-commit/rb58853/mcp-oauth.svg?style=flat)](https://github.com/rb58853/mcp-oauth/commits)
[![Commit activity](https://img.shields.io/github/commit-activity/m/rb58853/mcp-oauth)](https://github.com/rb58853/mcp-oauth/commits)
[![Stars](https://img.shields.io/github/stars/rb58853/mcp-oauth?style=flat&logo=github)](https://github.com/rb58853/mcp-oauth/stargazers)
[![Forks](https://img.shields.io/github/forks/rb58853/mcp-oauth?style=flat&logo=github)](https://github.com/rb58853/mcp-oauth/network/members)
[![Watchers](https://img.shields.io/github/watchers/rb58853/mcp-oauth?style=flat&logo=github)](https://github.com/rb58853/mcp-oauth)
[![Contributors](https://img.shields.io/github/contributors/rb58853/mcp-oauth)](https://github.com/rb58853/mcp-oauth/graphs/contributors)

</div>

This repository constitutes an OAuth system in Python that implements both server and client, following an OAuth authentication flow that integrates in a standard way with `FastMCP`. As a base, it uses the OAuth system from the official repository [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples).

## Table of Contents

* [Overview](#overview)
* [Installation](#installation)
* [Usage Example](#usage-example)
* [Developer Documentation](#developer-documentation)
* [Version History](#version-history)
* [Project Status](#project-status)
* [License](#license)

## Overview

This project represents a simple and extensible OAuth system in Python, integrated as much as possible with MCP standards and practices. Its goal is to facilitate the use of the OAuth system for MCP. It is integrated with the official MCP Python SDK (`"mcp[cli]"`), following the source code standard that provides the basis for the entire authorization system used and controlled by `FastMCP`.

Both an OAuth server and client are implemented, respecting the most common standards to maintain standardization. It is important to highlight that the OAuth server standard in the MCP context is still poorly defined and with scarce documentation, so the greatest possible standardization has been sought both in the server and client code.

This repository starts from the Antropic example in the [official repository](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples), modifying and restructuring the code to achieve optimal organization, facilitating practical and easy use when installing this repository as a pip package.

## Installation

To install the MCP client, you can use pip:

```shell
pip install mcp-oauth
```

## Usage Example

The examples presented are based on a FastMCP with `httpstream` transfer protocol. The shown code is illustrative and not fully compilable. For complete and compilable examples, please check the [tests](./tests/readme.md).

### OAuth Server

#### QuickOAuthServerHost

For a rapid deployment, the [`QuickOAuthServerHost`](src/mcp_oauth/server/quick_server.py) class can be utilized. This class initializes the `SimpleOAuthServerHost` with the necessary configuration for the OAuth server.

**Parameters:**

* `oauth_host (str)`: Specifies the host address for the OAuth server.
* `oauth_port (int)`: Defines the port number for the OAuth server.
* `superusername (str | None)`: Indicates the superuser username required for authentication.
* `superuserpassword (str | None)`: Represents the superuser password required for authentication.

``` python
# oauth_server.py
import click
from mcp_oauth import QuickOAuthServerHost

@click.command()
@click.option("--host", default="127.0.0.1", help="")
@click.option("--port", default=9080, help="Port to listen on")
@click.option("--superusername", default=None, help="")
@click.option("--superuserpassword", default=None, help="")
def main(
    host: str,
    port: int,
    superusername: str | None,
    superuserpassword: str | None,
):
    simple_oauth_server_host: QuickOAuthServerHost = QuickOAuthServerHost(
        oauth_port=port,
        oauth_host=host,
        superusername=superusername,
        superuserpassword=superuserpassword,
    )
    simple_oauth_server_host.run_oauth_server()


if __name__ == "__main__":
    main()
```

#### Manual Configuration

Alternatively, a manual configuration can be applied to customize the server according to specific requirements. In this scenario, an OAuth server integrated with the FastMCP server is created. The following example demonstrates how to start an OAuth server at the address `http://127.0.0.1:9000`.

```python
import os
from mcp_oauth import (
    OAuthServer,
    SimpleAuthSettings,
    AuthServerSettings,
)

def run_oauth_server():
    server_settings: AuthServerSettings = AuthServerSettings(
        host="127.0.0.1",
        port=9000,
        server_url="http://127.0.0.1:9000",
        auth_callback_path="http://127.0.0.1:9000/login",
    )
    auth_settings: SimpleAuthSettings = SimpleAuthSettings(
        superusername=os.getenv("SUPERUSERNAME"),
        superuserpassword=os.getenv("SUPERUSERPASSWORD"),
        mcp_scope="user",
    )
    oauth_server: OAuthServer = OAuthServer(
        server_settings=server_settings, auth_settings=auth_settings
    )
    oauth_server.run_starlette_server()
```

### MCP Server

A simple MCP server integrated with the OAuth server is created. For this integration, the OAuth server address must be provided when creating the MCP server, along with an `IntrospectionTokenVerifier`, as shown below:

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from mcp_oauth import IntrospectionTokenVerifier

class ServerSettings(BaseSettings):
    """Configuration for the MCP Server."""
    model_config = SettingsConfigDict(env_prefix="MCP_RESOURCE_")
    host: str = "localhost"
    port: int = 8000
    server_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8000")
    auth_server_url: AnyHttpUrl = AnyHttpUrl("http://localhost:9000")
    auth_server_introspection_endpoint: str = "http://localhost:9000/introspect"
    mcp_scope: str = "user"
    oauth_strict: bool = False

def create_mcp_server(settings: ServerSettings = ServerSettings()) -> FastMCP:
    token_verifier = IntrospectionTokenVerifier(
        introspection_endpoint=settings.auth_server_introspection_endpoint,
        server_url=str(settings.server_url),
        validate_resource=settings.oauth_strict,
    )
    
    name: str = "example-server"
    resource_server_url: str = f"{settings.server_url}{name}"

    mcp: FastMCP = FastMCP(
        name=name,
        instructions="This server specializes in private operations of user profiles data",
        debug=True,
        # Auth configuration for RS mode
        token_verifier=token_verifier,
        auth=AuthSettings(
            issuer_url=settings.auth_server_url,
            required_scopes=[settings.mcp_scope],
            resource_server_url=AnyHttpUrl(resource_server_url),
        ),
    )

    @mcp.tool(
        name="set_user_profile",
        description="Sets user profile information in the database",
    )
    async def set_user_profile(data: dict) -> dict:
        """Sets user profile information in the database for a user_id"""
        return {
            "status": "success",
            "message": "User successfully added to the dataset",
            "data": data,
        }
    return mcp
```

> **🚨 Important Note:** When setting up the OAuth server, it is essential to provide the full OAuth server URL (excluding the `"/mcp"` suffix) in the MCP Server configuration under the parameter `auth.resource_server_url`. It is common when deploying MCP instances with FastAPI to mount a router at the API root path. Therefore, the `resource_server_url` should be set as `api_root/new_router`, where `new_router` matches the path used in `fastapp.mount("/new_router", mcp_server.streamable_http_app())`.

### Client

To create a client, import `OAuthClient` and provide the following arguments:

* `client_name (str)`: client application name.
* `server_url (str)`: MCP server address (not the OAuth server).
* `body (dic[str,any] | None)`: When submitting data via a POST request, the request body typically contains the form data in JSON format. For example: `{ "username": "user", ... }`; this allows the client to send structured information such as user credentials or other form fields as part of the request payload.

This client is designed to facilitate the internal process. It is only necessary to configure the above and pass the associated `.oauth` property to the `streamablehttp_client`, as exemplified below:

```python
from mcp.client.session import ClientSession
from mcp_oauth import OAuthClient
import asyncio
from datetime import timedelta
from mcp.client.streamable_http import streamablehttp_client


def sample_mcp_client():
    server_url: str = "http://127.0.0.1:8000/example-server/mcp"
    oauth_client: OAuthClient = OAuthClient(
        client_name="sample_client",
        mcp_server_url=server_url,
        body=None
    )

    async def open_session():
        print("📡 Opening StreamableHTTP connection with authentication...")
        async with streamablehttp_client(
            url=server_url,
            auth=oauth_client.oauth,
            timeout=timedelta(seconds=60),
        ) as (read_stream, write_stream, get_session_id):
            print("🤝 Initializing MCP session...")
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✨ Session initialization complete!")
                print(f"\n✅ Connected to MCP server at {server_url}")
                if get_session_id:
                    session_id = get_session_id()
                    if session_id:
                        print(f"Session ID: {session_id}")
                tools = await session.list_tools()
                print("\n⚙️  Available tools")
                for tool in tools.tools:
                    print(f"   • {tool.name}: {tool.description}")

    asyncio.run(open_session())
```

## Developer Documentation

The developer documentation exposes the functionalities and project flow, facilitating understanding for external developers who want to update or extend the code. Currently, this documentation is being written and is not fully available. It can be provisionally consulted [here](./doc/development.md).

## Current Status / Main Features

* 🛠️ **Simple In-Memory OAuth Server:**  
  Authentication via superuser credentials with POST (auto) and GET (HTML login) methods; no refresh tokens yet.

* 🤖 **Automated OAuth Client:**  
  Auto login with auth-servers; supports POST requests with body dictionary for login; auto-detects OAuth server from MCP URL with option to override.

* 🔐 **Token Storage & Security:**  
  Encrypted token storage using `jose-python`; basic exception handling including null encryption key warnings.

* 🚀 **Dev Convenience:**  
  Includes `QuickOAuthServerHost` class to simplify OAuth server setup; fixes minor bugs and auto-loads local environment variables before starting.

[See changelog](./changelog.md)

## Project Status

> ⚠️ **Important Notice:** This project is in active development. Therefore, errors or unexpected behaviors may occur during its use.

## Contribution

Healthy and practical contributions from the community are welcome. This repository is basic and scalable, open to continuous modifications due to the constant evolution of the OAuth system in MCP and its standards. To contribute, it is recommended to fork the project and open a Pull Request detailing the proposed changes.

## License

MIT License. See [`license`](license).

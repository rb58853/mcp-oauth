# Client

## MCP Client

The MCP Client is responsible for managing client operations within the MCP ecosystem. In this particular use case, the MCP Client connects with the OAuth Client to request access to protected resources. It is responsible for initiating the OAuth authentication flow.

## OAuth Client

The OAuth Client is the entity that requests access to protected resources on behalf of a user or itself. This component implements the necessary authentication flows to obtain access tokens from the OAuth Server. Its main functions include:

- Redirecting the user to the authorization server.
- Handling authorization codes and tokens received.
- Secure storage of tokens.
- Automatic token renewal using the refresh token flow.

The OAuth Client is designed to be easily integrated into external applications requiring federated authentication.

## OAuth Client Provider

The OAuth Client Provider is responsible for the configuration and management of OAuth client credentials. This module facilitates the administration of client identifiers (`client_id`), secrets (`client_secret`), and authorized redirect URLs. Additionally, it implements mechanisms for credential rotation and secure management of sensitive information associated with each registered client.

## Callback Functions

The **Callback Functions** component is fundamental for managing the OAuth authentication flow, as it allows capturing and processing the authorization server's response after the user's redirection. This module implements a lightweight HTTP server that listens for OAuth redirects and extracts relevant parameters such as the authorization code and state, thus facilitating integration with desktop clients or automated scripts.

### Objective

The main objective of [this component](../src//mcp_oauth/client/features/callbacks.py) is to provide a simple, secure, and reusable infrastructure to handle OAuth callbacks in Python applications, enabling automation of the authorization flow without relying on complex web frameworks.

### Main Components

#### 1. CallbackHandler

`CallbackHandler` is a subclass of `BaseHTTPRequestHandler` that implements the logic to receive and process GET requests sent to the callback endpoint. Its responsibilities include:

- **OAuth redirection processing:** Captures the `code`, `state`, and `error` parameters sent by the OAuth server after user authentication. This occurs in the `do_GET()` method; when a GET request is made to the callback server, the `do_GET()` method is called, and the request is delegated to the client using the `redirect_uri` pointing to this callback server.

- **Data management:** Saves relevant data in a shared dictionary for later retrieval by the client, from within the `do_GET()` method.

#### 2. CallbackServer

`CallbackServer` encapsulates the logic for initializing, running, and stopping a local HTTP server that uses the `CallbackHandler`. Its main features include:

- **Background execution:** Starts the server in a separate thread, allowing the main application to continue running.
- **Lifecycle management:** Provides methods to start (`start`), stop (`stop`), and wait for the callback (`wait_for_callback`) with timeout handling.
- **Secure storage:** Internally stores the authorization code, state, and possible errors for later querying.
<!-- - **Flexible configuration:** Allows specifying the listening port and maximum wait time. -->

#### 3. CallbackFunctions

`CallbackFunctions` is a high-level class that orchestrates the use of `CallbackServer` and exposes methods to facilitate the OAuth authentication flow. Its functionalities include:

- **Parametrizable initialization:** Allows configuring username, password, port, site security, and timeout.
- **Callback handling:** The `callback_handler` method waits for the authorization code and state to arrive, stopping the server once received.
- **Automatic redirection:** The `_default_redirect_handler` method opens a web browser or performs an automated POST request depending on the configuration and presence of credentials.
- **Security validation:** Verifies that the authorization URL is secure before proceeding, especially in production environments.

#### 4. Utility: get_params_from_uri

Auxiliary function that extracts and returns query parameters from a URL, facilitating data manipulation and transmission during the authentication flow.

### Usage Flow

1. **Start the callback server:** When starting the authorization process, the `CallbackServer` is launched on a local port.
2. **User redirection:** The user is redirected to the OAuth authorization server, either automatically or by opening a browser.
3. **Response reception:** The callback server captures the redirect with the `code` and `state` parameters.
4. **Processing and shutdown:** The authorization code is stored and the server is stopped, allowing the client to continue the token exchange flow.

### Advantages and Considerations

- **Simplicity:** Enables handling OAuth callbacks without relying on external frameworks.
- **Automation:** Supports both manual flows (browser) and automated flows (POST requests).
- **Security:** Includes validations to prevent redirection to insecure sites.
- **Extensibility:** Easily adaptable to different OAuth authentication scenarios.

This component is essential for any OAuth integration in Python applications that require capturing the authorization server's response locally and securely, facilitating both development and automation of testing and deployments.

### TokenVerifier (Server Core)

The TokenVerifier is a central component in the OAuth server responsible for validating access and refresh tokens issued by the system. Its main responsibilities include:

- Verifying the signature and temporal validity of tokens.
- Checking permissions and scopes associated with each token.
- Detecting and preventing the use of revoked or expired tokens.
- Providing detailed responses in case of authentication or authorization errors.

The TokenVerifier is essential to maintain the security and reliability of the authentication system.

### TokenStorage (Client Core)

TokenStorage is the module responsible for managing and securely storing tokens on the client side. Its functionalities include:

- Encrypted storage of access and refresh tokens.
- Handling token expiration and automatic renewal.
- Secure deletion of revoked or expired tokens.
- Integration with persistent storage systems (files, databases, etc.).

This component ensures tokens are available when needed while maintaining high standards of security and confidentiality.

---

### `async_auth_flow` (OAuthClient)

This method handles the entire authorization flow from the client side ([`SimpleOAuthClientProvider`](../src/mcp_oauth/client/client_provider/client_provider.py)). In this repository, this method was overridden from the original to allow custom control of the flow from our client without modifying any source code of our OAuthServer. This way, the OAuth server remains standard without changes, and the client code has flexible modifications while still complying with standard connections.

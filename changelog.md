# Version History 📜

## v0.0.5 🚀

* OAuth server detection is now performed within the client flow. A fix was applied to resolve issues with OAuth server path handling to ensure proper functionality.
* The client now accepts a `body` parameter, which is a dictionary sent in POST requests. If `body` is provided and not `None`, its values are included in the POST request payload.

## v0.0.4 🔍

* OAuth server detection is now automatic. Providing the MCP server alone is sufficient to identify the corresponding OAuth server.
* Optionally, you can still specify the OAuth server URL manually, which will override the automatic detection based on the MCP server.

## v0.0.3 🛠️

* Implemented the `QuickOAuthServerHost` class to simplify OAuth server creation.
* Added exception handling, including guidance for handling a null cryptography key scenario.

## v0.0.2 🐞

* Fixed minor typographical errors in secure URLs.
* Added the `loadenv` function before any loading processes to ensure local environment variables are always loaded.
* Included necessary package dependencies.

## v0.0.1 ⚙️

* Developed a simple OAuth server running in memory.
* Refresh tokens are not included in this version.
* Supports authentication via superuser credentials (username and password).
* Utilizes `"POST"` method for automatic login using credentials from environment variables, and `"GET"` for login via an HTML page.
* Automated OAuth client that performs re-login on authorization failures.
* Simple token storage on the filesystem with encryption using `jose-python`.

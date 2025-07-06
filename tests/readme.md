# Tests

The testing system is designed to independently launch two servers and, additionally, connect a client with the generated MCP server and the generated OAuth server. The testing flow follows the steps below in the specified order:

- Launch the `OAuthServer` on a specific host.
- Launch the `FastMCP` server and associate it with this host.
- Run a client that connects to these servers and verify that the authorization process works correctly.

To facilitate usage, it is recommended to use the `.vscode/launch.json` file, which enables parallel execution of each service. If preferring to run this code by other means, it is essential to ensure that each step runs in parallel rather than sequentially.

The file [`testing.py`](./testing.py) contains all the necessary functions to run each service.

If one wishes to run the tests using the repository's source code directly, either for testing or modifying the code, access the `dev` branch. Within this branch, the folder `src/mcp_auth/tests` is available where the tests can be executed. Execution options are also optionally provided in `.vscode/launch.json`.

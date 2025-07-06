# Server

## MCP Server

The MCP Server is responsible for managing the internal operations of the MCP server. In the specific context of this repository, the MCP Server acts as an intermediary between internal services and the associated `OAuthServer`. Its main function here is to establish and maintain a secure connection with the OAuth server, requesting and managing the authorization needed to access protected resources.

## OAuth Server

The OAuth Server is the core of the project. Its primary function is to manage the registration, validation, and administration of clients and users interacting with the system. Its responsibilities include:

- Registration and management of client applications.
- Authentication of users and clients.
- Issuance, validation, and revocation of access and refresh tokens.
- Secure storage of credentials and tokens.

The OAuth Server is designed to be extensible and secure, following best practices in authentication and authorization. Currently, it is under development and only operates in RAM.

## OAuth Server Provider

The OAuth Server Provider is the component responsible for implementing the specific logic of the OAuth provider. This module defines security policies, supported authentication methods, and rules for token issuance and validation. It allows integration with external identity systems (LDAP, databases, etc.) and facilitates customization of the OAuth server behavior according to project requirements.

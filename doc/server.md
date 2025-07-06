# OAuth Server

## MCP Server

El MCP Server es responsable de gestionar las operaciones internas del servidor MCP. En el contexto específico de este repositorio, el MCP Server actúa como intermediario entre los servicios internos y el `OAuthServer` asociado. En este contexto, su principal función es establecer y mantener una conexión segura con el servidor OAuth, solicitando y gestionando la autorización necesaria para acceder a los recursos protegidos.

## OAuth Server

El OAuth Server constituye el núcleo del proyecto. Su función principal es la de gestionar el registro, validación y administración de los clientes y usuarios que interactúan con el sistema. Entre sus responsabilidades se encuentran:

- Registro y gestión de aplicaciones clientes.
- Autenticación de usuarios y clientes.
- Emisión, validación y revocación de tokens de acceso y refresco.
- Almacenamiento seguro de credenciales y tokens.
<!-- - Implementación de los distintos flujos de OAuth2 (Authorization Code, Client Credentials, etc.). -->

El OAuth Server está diseñado para ser extensible y seguro, siguiendo las mejores prácticas en materia de autenticación y autorización. Actualemente se encuentra en proceso de desarrollo y solo funciona en memoria ram.

## OAuth Server Provider

El OAuth Server Provider es el componente encargado de implementar la lógica específica del proveedor OAuth. Este módulo define las políticas de seguridad, los métodos de autenticación soportados, y las reglas para la emisión y validación de tokens. Permite la integración con sistemas de identidad externos (LDAP, bases de datos, etc.) y facilita la personalización del comportamiento del servidor OAuth según los requerimientos del proyecto.

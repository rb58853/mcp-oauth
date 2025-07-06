# OAuth Client

## MCP Client

El MCP Client se encarga de gestionar las operaciones del cliente dentro del ecosistema MCP. En este caso de uso particular, el MCP Client se conecta con el OAuth Client para solicitar acceso a los recursos protegidos. Es responsable de iniciar el flujo de autenticación OAuth.

## OAuth Client

El OAuth Client es la entidad que solicita acceso a los recursos protegidos en nombre de un usuario o de sí mismo. Este componente implementa los flujos de autenticación necesarios para obtener los tokens de acceso desde el OAuth Server. Sus principales funciones incluyen:

- Redirección del usuario al servidor de autorización.
- Manejo de los códigos de autorización y tokens recibidos.
- Almacenamiento seguro de los tokens.
- Renovación automática de tokens mediante el flujo de refresh token.

El OAuth Client está diseñado para ser fácilmente integrable en aplicaciones externas que requieran autenticación federada.

## OAuth Client Provider

El OAuth Client Provider es responsable de la configuración y gestión de las credenciales del cliente OAuth. Este módulo facilita la administración de los identificadores de cliente (`client_id`), secretos (`client_secret`), y las URLs de redirección autorizadas. Además, implementa mecanismos para la rotación de credenciales y la gestión segura de la información sensible asociada a cada cliente registrado.

## Callback Functions

El componente de **Callback Functions** es fundamental para la gestión del flujo de autenticación OAuth, ya que permite capturar y procesar la respuesta del servidor de autorización tras la redirección del usuario. Este módulo implementa un servidor HTTP ligero que escucha las redirecciones OAuth y extrae los parámetros relevantes, como el código de autorización y el estado, facilitando así la integración con clientes de escritorio o scripts automatizados.

### Objetivo

El objetivo principal de [este componente](../src//mcp_oauth/client/features/callbacks.py) es proporcionar una infraestructura simple, segura y reutilizable para manejar callbacks OAuth en aplicaciones Python, permitiendo la automatización del flujo de autorización sin depender de frameworks web complejos.

### Componentes Principales

#### 1. CallbackHandler

`CallbackHandler` es una subclase de `BaseHTTPRequestHandler` que implementa la lógica para recibir y procesar las solicitudes GET enviadas al endpoint de callback. Sus responsabilidades incluyen:

- **Procesamiento de la redirección OAuth:** Captura los parámetros `code`, `state` y `error` enviados por el servidor OAuth tras la autenticación del usuario. Esto ocurre en el metodo `do_GET()`, se hace una redireccion al servidor callback, y en el momento que se hace una peticion get se llama al metodo `do_GET()`, la peticion de este se delega al cliente, usando la `redirect_uri` que apunta a este servidor callback.

- **Gestion de datos:** Guarda los datos relevantes en un diccionario compartido para su posterior recuperación por el cliente. Desde el metodo `do_GET()`

#### 2. CallbackServer

`CallbackServer` encapsula la lógica de inicialización, ejecución y parada de un servidor HTTP local que utiliza el `CallbackHandler`. Sus principales características son:

- **Ejecución en segundo plano:** Inicia el servidor en un hilo separado, permitiendo que la aplicación principal continúe su ejecución.
- **Gestión de ciclo de vida:** Proporciona métodos para iniciar (`start`), detener (`stop`) y esperar la llegada de la callback (`wait_for_callback`) con manejo de timeout.
- **Almacenamiento seguro:** Mantiene de forma interna el código de autorización, el estado y posibles errores para su consulta posterior.
<!-- - **Configuración flexible:** Permite especificar el puerto de escucha y el tiempo máximo de espera. -->

#### 3. CallbackFunctions

`CallbackFunctions` es una clase de alto nivel que orquesta el uso de `CallbackServer` y expone métodos para facilitar el flujo de autenticación OAuth. Entre sus funcionalidades se destacan:

- **Inicialización parametrizable:** Permite configurar usuario, contraseña, puerto, seguridad del sitio y tiempo de espera.
- **Manejo del callback:** El método `callback_handler` espera la llegada del código de autorización y el estado, deteniendo el servidor una vez recibidos.
- **Redirección automática:** El método `_default_redirect_handler` abre el navegador web o realiza una petición POST automatizada, dependiendo de la configuración y la presencia de credenciales.
- **Validación de seguridad:** Verifica que la URL de autorización sea segura antes de proceder, especialmente en ambientes de producción.

#### 4. Utilidad: get_params_from_uri

Función auxiliar que extrae y retorna los parámetros de consulta de una URL, facilitando la manipulación y el envío de datos en el flujo de autenticación.

### Flujo de Uso

1. **Inicio del servidor de callback:** Al iniciar el proceso de autorización, se levanta el `CallbackServer` en un puerto local.
2. **Redirección del usuario:** El usuario es redirigido al servidor de autorización OAuth, ya sea automáticamente o mediante la apertura de un navegador.
3. **Recepción de la respuesta:** El servidor de callback captura la redirección con los parámetros `code` y `state`.
4. **Procesamiento y cierre:** El código de autorización es almacenado y el servidor es detenido, permitiendo que el cliente continúe el flujo de intercambio de tokens.

### Ventajas y Consideraciones

- **Simplicidad:** Permite manejar callbacks OAuth sin depender de frameworks externos.
- **Automatización:** Soporta tanto flujos manuales (navegador) como automatizados (peticiones POST).
- **Seguridad:** Incluye validaciones para evitar redirecciones a sitios no seguros.
- **Extensibilidad:** Puede adaptarse fácilmente a distintos escenarios de autenticación OAuth.

---

### Ejemplo de Uso

```python
from callback_module import CallbackFunctions

# Inicialización del componente
callback = CallbackFunctions(username="usuario", password="contraseña", port=3030)

# Lanzar el flujo de autenticación y esperar el callback
authorization_code, state = await callback.callback_handler()
```

Este componente es esencial para cualquier integración OAuth en aplicaciones Python que requieran capturar la respuesta del servidor de autorización de manera local y segura, facilitando tanto el desarrollo como la automatización de pruebas y despliegues.

### TokenVerifier (Server Core)

El TokenVerifier es un componente central en el servidor OAuth encargado de la validación de los tokens de acceso y refresco emitidos por el sistema. Sus principales responsabilidades incluyen:

- Verificar la firma y validez temporal de los tokens.
- Comprobar los permisos y alcances (`scopes`) asociados a cada token.
- Detectar y prevenir el uso de tokens revocados o caducados.
- Proveer respuestas detalladas en caso de errores de autenticación o autorización.

El TokenVerifier es esencial para mantener la seguridad y confiabilidad del sistema de autenticación.

### TokenStorage (Client Core)

El TokenStorage es el módulo encargado de la gestión y almacenamiento seguro de los tokens en el lado del cliente. Entre sus funcionalidades destacan:

- Almacenamiento cifrado de tokens de acceso y refresco.
- Manejo de la expiración y renovación automática de tokens.
- Eliminación segura de tokens revocados o caducados.
- Integración con sistemas de almacenamiento persistente (archivos, bases de datos, etc.).

Este componente garantiza que los tokens estén disponibles para su uso cuando sea necesario, manteniendo altos estándares de seguridad y confidencialidad.

---

### `async_auth_flow` (OAuthClient)

Este es el metodo encargado de todo el flujo de autorizacion desde la parte del cliente ([`SimpleOAuthClientProvider`](../src/mcp_oauth/client/client_provider/client_provider.py)). En este repositorio, este metodo fue sobreescrito desde e metodo original para poder controlar a gusto el flujo desde nuestro cliente sin tocar nada del codigo fuente de nuestro OAuthServer. De esta forma se logra que el Oauth server sea estandar sin cambios y el codigo del cliente posee cambios maleables pero a su vez tambien cumple con conexiones estandars.

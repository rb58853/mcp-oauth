# Documentacion para desarrolladores

ESta documentacion es una comprension basica de la lectura y debug del codigo fuente del paquete oauth referente a `"mcp[cli]"`. Usa como base [el ejemplo de la pagina oficial](), al cual se le ha dedicado tiempo para comprender el flujo tanto propio como el del codigo fuente que utiliza, y desde aqui compartir la experiencia de esta lectura y comprension del flujo OAuth del codigo fuente y de ejemplo.

## Flujo

Para comprender el flujo hay que tener en cuenta varios conceptos:

- MCP server
- MCP client
- Oauth Server
- Oauth Provider
- Oauth Client
- TokenStorage
- TokenVerifier

### Flujo paso a paso

El flujo del sistema oauth comienza en la aplicacion cliente, el [cliente oauth](../src/mcp_oauth/client/oauth_client.py)

## Metodos y endpoints de Oauth server

A continuacion se exponen algunos de los endpoints y metodos  que mas dificultad de comprension tuvieron para mi. Ya que muchos de ellos estan encapsulados en un flujo interno que necesita lectura y comprension del codigo fuente.

### `/autorize` endpoint

Este endpoint lo que hace s redirigir hacia el metodo [`provider.autorize`](../src/mcp_oauth/server/auth_provider/simple_auth_provider.py) y todo el control del request es parte del autorize del sdk de python. Este metodo acepta tanto `"POST"` como `"GET"`, siempre se le debe pasar el client_id y el state. Para meor comprension leease el codigo fuente.

Este es el metodo llamado desde el [_default_redirect_handler](../src/mcp_oauth/client/features/callbacks.py) del cliente para abrir una url. Ya que no se puede tocar el codigo fuente, la solucion adoptada fue tratar este problema desde el cliente. Entonces hay dos opciones de autenticacion, una es abriendo el navegador en el endpoint autorize, esta opcion te muesttra una pantalla de login, aqui debes poner credenciales validos de usuario y contrasenna; la otra opcion es automatica, el codigo conoce las credenciales, desde este se le pasan en una peticion post, se pide que no redrija el flujo para que el codigo fuente no lo convoerta en una peticion GET, luego con ello obtiene como response una location que es exactamente el endpoint al cual se le debe hacer la peticion post, seguido a esto se hace dicha peticion con los credenciales pasados por data.

<figure>
  <img src="./images/autorize.png" alt="Codigo fuente" />
  <figcaption>Codigo fuente del flujo al llamado al endpoint <b>/autorize</b></figcaption>
</figure>

### Others

## Client

En el flujo OAuth moderno, es el cliente quien tiene la responsabilidad de renovar el token. El servidor OAuth simplemente valida los tokens recibidos en cada petición y, si el token es inválido o ha expirado, responde con un error (por ejemplo, HTTP 401 o 403), pero no redirecciona automáticamente al cliente ni inicia un nuevo flujo de autorización.

# Documentacion para desarrolladores

ESta documentacion es una comprension basica de la lectura y debug del codigo fuente del paquete oauth referente a `"mcp[cli]"`. Usa como base [el ejemplo de la pagina oficial](), al cual se le ha dedicado tiempo para comprender el flujo tanto propio como el del codigo fuente que utiliza, y desde aqui compartir la experiencia de esta lectura y comprension del flujo OAuth del codigo fuente y de ejemplo.

> ### ⚠️ WARNING Esta documentacion esta muy basica y pobre aun, se esta trabajando en mejorar la misma

### Contenido

- [Oauth Server](oauth_server.md)
- [Oauth Client](oauth_client.md)
- [Flow](#flow)

## Flow

El flujo del sistema oauth comienza en la aplicacion cliente, el [cliente oauth](../src/mcp_oauth/client/oauth_client.py)

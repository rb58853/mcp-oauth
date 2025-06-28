import requests
from urllib.parse import urlencode
from mcp.server.auth.routes import (
    AUTHORIZATION_PATH,
    REGISTRATION_PATH,
    TOKEN_PATH,
    REVOCATION_PATH,
)


class OAuthClient:
    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        client_name: str | None = "my_client",
        redirect_uri: str | None = "http://127.0.0.1:8080",
        server_url: str | None = "http://127.0.0.1:9000",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_name = client_name
        self.redirect_uri = redirect_uri

        # url paths
        self.server_url = server_url
        self.auth_url = server_url + AUTHORIZATION_PATH
        self.token_url = server_url + TOKEN_PATH
        self.register_url = server_url + REGISTRATION_PATH
        self.revoke_url = server_url + REVOCATION_PATH

        # sesion
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None

    def register(self):
        """Registra un usuario si el proveedor lo permite (opcional)."""
        if not self.register_url:
            raise NotImplementedError("El endpoint de registro no está configurado.")

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "client_name": self.client_name,
            "redirect_uris": [self.redirect_uri],
        }

        response = self.session.post(self.register_url, json=data)
        response.raise_for_status()
        self.client_id = response.json["client_id"]
        self.client_secret = response.json["client_secret"]
        return response.json()

    def get_client_info(self):
        """"""
        user_url: str = self.auth_url
        params = {
            "client_id": self.client_id,
        }

        response = self.session.get(user_url, params=params)
        response.raise_for_status()
        return response.json()


def main():
    # Configuración del cliente OAuth
    client = OAuthClient(
        client_name="my_test_client",
    )
    # 1. (Opcional) Registrar usuario demo
    try:
        print("Registrando usuario my_user...")
        user = client.register()
        print("Usuario registrado:", user)
    except Exception as e:
        print("Registro omitido o ya existente:", e)


if __name__ == "__main__":
    main()

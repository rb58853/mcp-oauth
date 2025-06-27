import json


class Settings:
    def __init__(self):
        with open("oauth.settings.json", "r") as file:
            settings_file: dict[str, any] = json.load(file)

        self.username = settings_file.get("username", "user")
        self.password = settings_file.get("password", "password")
        self.port = settings_file.get("port", 9000)
        self.service_documentation_url = settings_file.get(
            "service_documentation_url", None
        )
        self.scopes = settings_file.get("scopes", [])
        pass


settings = Settings()

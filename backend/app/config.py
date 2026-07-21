from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "change-me-intnetwork-default-secret"
APP_VERSION = "1.30.0"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str = DEFAULT_SECRET_KEY
    database_url: str = "sqlite:///./intnetwork.db"
    admin_email: str = "trainer@example.com"
    admin_password: str = ""  # nur Bootstrap: seedet EINEN Trainer bei leerer trainer-Tabelle; danach in DB gepflegt
    debug: bool = False
    # Kommaseparierte erlaubte Frontend-Origins für CORS. In Prod auf die echte
    # Domain setzen (z.B. "https://kurs.example.com"); Default = lokale Entwicklung.
    allowed_origins: str = "http://localhost:5173"
    # Ansible-Lab: nur aktiv, wenn BEIDE Werte gesetzt sind. Ohne Runner
    # antwortet /api/lab mit 503 und das Widget zeigt einen Hinweis — der Kurs
    # funktioniert weiter. Der Runner laeuft absichtlich in einem eigenen
    # Container ohne Geheimnisse und ohne Weg ins Internet (siehe runner/app.py).
    lab_runner_url: str = ""
    lab_runner_token: str = ""
    lab_timeout_seconds: int = 30

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = Settings()

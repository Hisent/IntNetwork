from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "change-me-intnetwork-default-secret"
APP_VERSION = "1.11.0"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str = DEFAULT_SECRET_KEY
    database_url: str = "sqlite:///./intnetwork.db"
    admin_email: str = "trainer@example.com"
    admin_password: str = ""  # nur Bootstrap: seedet EINEN Trainer bei leerer trainer-Tabelle; danach in DB gepflegt
    debug: bool = False


settings = Settings()

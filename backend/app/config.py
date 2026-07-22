from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "change-me-intnetwork-default-secret"
APP_VERSION = "1.35.0"


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
    # Ansible-Lab: nur aktiv, wenn dieses Verzeichnis gesetzt ist und ein
    # in/-Unterordner existiert (gemeinsames Volume mit dem Runner). Ohne das
    # antwortet /api/lab mit 503 und das Widget zeigt einen Hinweis — der Kurs
    # funktioniert weiter. Der Runner-Container hat network_mode: none, also
    # gar kein Netz; der Austausch laeuft ueber Dateien (siehe runner/worker.py).
    lab_queue_dir: str = ""
    lab_timeout_seconds: int = 30
    # Welche Auftragsarten /api/lab/status als nutzbar meldet (Kommaseparation,
    # z.B. "ansible,openssl"). ACHTUNG: Das Backend kennt die Freigabe des
    # Runners (dessen RUNNER_KINDS) nicht automatisch — diese Einstellung ist
    # keine Abfrage des Runner-Zustands, sondern eine eigene Angabe, die beim
    # Ausrollen von Hand parallel zu RUNNER_KINDS gepflegt werden muss.
    lab_kinds: str = "ansible"
    # Trainer-Passkey-Anmeldung (WebAuthn), Zusatz zum Passwort: nur aktiv, wenn
    # RP-ID und Origin BEIDE gesetzt sind (siehe app/services/passkey.py).
    # RP-ID und Origin müssen der von außen sichtbaren Adresse entsprechen
    # (hinter Traefik NICHT der Containername!) -- der Browser bindet den
    # Passkey an genau diese Domain. Ein späterer Domainwechsel macht alle
    # registrierten Passkeys unbrauchbar; das ist Absicht des Verfahrens
    # (Phishing-Schutz), kein Fehler, und lässt sich nicht per Migration heilen.
    webauthn_rp_id: str = ""
    webauthn_rp_name: str = "IntLab"
    webauthn_origin: str = ""

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def lab_kinds_list(self) -> list[str]:
        return [k.strip() for k in self.lab_kinds.split(",") if k.strip()]


settings = Settings()

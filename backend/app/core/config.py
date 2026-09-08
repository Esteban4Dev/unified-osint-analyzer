from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración centralizada. Los valores se leen del archivo .env."""

    shodan_api_key: str = ""
    virustotal_api_key: str = ""
    hibp_api_key: str = ""
    securitytrails_api_key: str = ""

    database_url: str = "sqlite+aiosqlite:///./osint.db"
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def configured_sources(self) -> dict[str, bool]:
        """Indica qué fuentes tienen API key configurada."""
        return {
            "shodan": bool(self.shodan_api_key),
            "virustotal": bool(self.virustotal_api_key),
            "hibp": bool(self.hibp_api_key),
            "securitytrails": bool(self.securitytrails_api_key),
            "dnsdumpster": True,  # no requiere key, usa scraping best-effort
        }


settings = Settings()

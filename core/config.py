from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema de Gestión de Gastos"
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://localhost:60063/"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    EMAIL_ENABLED: bool = False
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "Expense Control"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @model_validator(mode="after")
    def validate_email_settings(self) -> "Settings":
        if self.EMAIL_ENABLED:
            missing: list[str] = []
            if not self.SMTP_HOST:
                missing.append("SMTP_HOST")
            if not self.SMTP_USER:
                missing.append("SMTP_USER")
            if not self.SMTP_PASSWORD:
                missing.append("SMTP_PASSWORD")
            if not self.SMTP_FROM_EMAIL:
                missing.append("SMTP_FROM_EMAIL")
            if missing:
                raise ValueError(f"Missing required email settings: {', '.join(missing)}")
        return self


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema de Gestión de Gastos"
    DATABASE_URL: str
    SECRET_KEY: str

    # Nueva forma de configurar el archivo .env en Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignora variables extra que haya en el .env
    )


settings = Settings()

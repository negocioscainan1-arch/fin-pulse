from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str | None = None
    news_api_key: str | None = None
    app_env: str = "local"
    refresh_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()

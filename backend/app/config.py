import os

class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    news_api_key: str | None = os.getenv("NEWS_API_KEY")
    app_env: str = os.getenv("APP_ENV", "local")
    refresh_minutes: int = int(os.getenv("REFRESH_MINUTES", "30"))

settings = Settings()

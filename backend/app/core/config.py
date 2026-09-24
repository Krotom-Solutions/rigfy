from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ZenRows
    zenrows_api_key: str = ""
    zenrows_base_url: str = "https://api.zenrows.com/v1/"

    # Database
    database_url: str

    # Scraper
    scraper_pages_per_run: int = 5
    scraper_delay_seconds: int = 2
    scraper_schedule_hour: int = 3
    scraper_schedule_minute: int = 0

    # App
    app_env: str = "development"
    log_level: str = "INFO"

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:4173",
        "https://rigfy.vercel.app",
        "https://rigfy.netlify.app",
        "*",
    ]


settings = Settings()

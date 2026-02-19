"""
Forkast API Configuration
Loads settings from environment variables / .env file
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Application
    app_name: str = "Forkast API"
    app_version: str = "1.0.0"
    debug: bool = False
    api_port: int = 8518
    streamlit_port: int = 8517

    # Database
    database_url: str = f"sqlite:///{Path(__file__).parent.parent / 'forkast.db'}"

    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_currency: str = "aed"

    # Authentication
    admin_api_key: str = "fk-admin-dev-key-change-me"
    api_key_prefix: str = "fk-pos-"

    # CORS
    cors_origins: list = ["http://localhost:8517", "http://localhost:8518"]

    model_config = {"env_file": ".env", "env_prefix": "FORKAST_"}


settings = Settings()

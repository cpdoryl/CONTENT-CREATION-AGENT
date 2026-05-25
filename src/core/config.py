"""Configuration management — loads from .env and validates API keys"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API Keys
    OPENAI_API_KEY: str
    ELEVENLABS_API_KEY: str
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"
    PERPLEXITY_API_KEY: str
    GOOGLE_CREDENTIALS_PATH: str = "credentials/google_credentials.json"
    GOOGLE_DRIVE_FOLDER_ID: str = ""
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    APIFY_API_TOKEN: str = ""
    JSON2VIDEO_API_KEY: str = ""

    # Content Config
    NICHE: str = "personal finance"
    TARGET_AUDIENCE: str = "millennials"
    BRAND_VOICE: str = "calm, direct, educational"
    BRAND_COLORS: str = "#1D9E75,#06132B,#F5F4F0"
    CONTENT_PER_WEEK: int = 5
    OUTPUT_DIR: str = "output"


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Chess Mentor AI"
    APP_VERSION: str = "0.1.0"

    STOCKFISH_PATH: str = "/opt/homebrew/bin/stockfish"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
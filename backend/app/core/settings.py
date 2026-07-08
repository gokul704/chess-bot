from pydantic_settings import BaseSettings
from app.core.settings import settings

class Settings(BaseSettings):
    APP_NAME: str = "Chess Bot AI"
    APP_VERSION: str = "0.1.0"

self.engine = chess.engine.SimpleEngine.popen_uci(
    settings.STOCKFISH_PATH
)
    class Config:
        env_file = ".env"


settings = Settings()
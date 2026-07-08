from fastapi import APIRouter

from app.services.game_analysis_service import GameAnalysisService
from pathlib import Path


router = APIRouter(
    prefix="/game",
    tags=["Game"],
)

game_service = GameAnalysisService()


BASE_DIR = Path(__file__).resolve().parents[4]
SAMPLE_GAME = BASE_DIR / "data" / "games" / "sample_game.pgn"


@router.get("/sample")
def analyze_sample_game():
    return game_service.load_game(str(SAMPLE_GAME))
from fastapi import APIRouter

from app.schemas.chess import (
    AnalyzeFenRequest,
    AnalysisResponse,
)
from app.services.stockfish_service import StockfishService

router = APIRouter(
    prefix="/chess",
    tags=["Chess"],
)

stockfish = StockfishService()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
)
def analyze(request: AnalyzeFenRequest):
    return stockfish.analyze_fen(request.fen)

@router.post("/evaluate")
def evaluate(request: AnalyzeFenRequest):
    return {
        "cp": stockfish.evaluate_fen(request.fen)
    }
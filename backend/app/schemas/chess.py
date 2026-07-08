from pydantic import BaseModel


class AnalyzeFenRequest(BaseModel):
    fen: str


class AnalysisResponse(BaseModel):
    best_move: str
    evaluation: str
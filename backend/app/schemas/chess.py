from pydantic import BaseModel


class AnalyzeFenRequest(BaseModel):
    fen: str


class Evaluation(BaseModel):
    type: str
    value: int
    display: str


class CandidateMove(BaseModel):
    move: str
    evaluation: str


class AnalysisResponse(BaseModel):
    best_move: str
    depth: int
    evaluation: Evaluation
    top_moves: list[CandidateMove]
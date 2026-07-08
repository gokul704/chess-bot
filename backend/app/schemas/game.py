from pydantic import BaseModel


class MoveAnalysis(BaseModel):
    move_number: int
    played_move: str
    fen: str
    best_move: str
    evaluation: str


class GameAnalysisResponse(BaseModel):
    white: str
    black: str
    result: str
    moves: list[MoveAnalysis]
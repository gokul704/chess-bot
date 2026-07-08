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

class MoveAnalysis(BaseModel):
    move_number: int

    played_move: str

    best_move: str

    evaluation_before: int

    evaluation_after: int

    centipawn_loss: int

    classification: str

    fen: str

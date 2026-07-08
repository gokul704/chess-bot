import chess
import chess.pgn

from app.services.stockfish_service import StockfishService
from app.utils.metrics import (
    calculate_centipawn_loss,
    classify_move,
)


class GameAnalysisService:

    def __init__(self):
        self.stockfish = StockfishService()

    def analyze_game(self, path: str):

        with open(path) as pgn:
            game = chess.pgn.read_game(pgn)

        board = game.board()

        analysis = []

        move_number = 1

        for move in game.mainline_moves():

            # Current position before the move
            fen = board.fen()

            # Rich analysis (best move, top moves)
            engine_analysis = self.stockfish.analyze_fen(fen)

            # Raw evaluation before move
            evaluation_before = self.stockfish.evaluate_fen(fen)

            # Player makes the move
            board.push(move)

            # New position after move
            evaluation_after = self.stockfish.evaluate_fen(board.fen())

            # Calculate Centipawn Loss
            cpl = calculate_centipawn_loss(
                evaluation_before,
                evaluation_after,
            )

            # Classify move
            classification = classify_move(cpl)

            analysis.append(
                {
                    "move_number": move_number,
                    "played_move": move.uci(),
                    "fen": fen,
                    "best_move": engine_analysis["best_move"],
                    "evaluation_before": evaluation_before,
                    "evaluation_after": evaluation_after,
                    "centipawn_loss": cpl,
                    "classification": classification,
                }
            )

            move_number += 1

        return {
            "white": game.headers["White"],
            "black": game.headers["Black"],
            "result": game.headers["Result"],
            "moves": analysis,
        }
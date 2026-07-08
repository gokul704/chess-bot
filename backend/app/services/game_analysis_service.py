import chess
import chess.pgn

from app.services.stockfish_service import StockfishService
from app.services.statistics_service import StatisticsService
from app.utils.metrics import (
    calculate_centipawn_loss,
    classify_move,
)
from app.utils.accuracy import calculate_accuracy

class GameAnalysisService:

    def __init__(self):
        self.stockfish = StockfishService()
        self.statistics = StatisticsService()

    def analyze_game(self, path: str):

        with open(path) as pgn:
            game = chess.pgn.read_game(pgn)

        board = game.board()

        analysis = []

        move_number = 1

        for move in game.mainline_moves():

            # Position before move
            fen = board.fen()

            # Best move analysis
            engine_analysis = self.stockfish.analyze_fen(fen)

            # Evaluation before move
            evaluation_before = self.stockfish.evaluate_fen(fen)

            # Play move
            board.push(move)

            # Evaluation after move
            evaluation_after = self.stockfish.evaluate_fen(board.fen())

            # Calculate CPL
            cpl = calculate_centipawn_loss(
                evaluation_before,
                evaluation_after,
            )

            # Classification
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

        # Calculate statistics AFTER all moves
        statistics = self.statistics.calculate(analysis)
        accuracy = calculate_accuracy(
        statistics["average_centipawn_loss"]
)

        return {
            "summary": {
                "white": game.headers["White"],
                "black": game.headers["Black"],
                "result": game.headers["Result"],
                "total_moves": len(analysis),
                "accuracy": accuracy,
            },
            "statistics": statistics,
            "moves": analysis,
        }
import chess
import chess.pgn

from app.services.stockfish_service import StockfishService
from app.services.statistics_service import StatisticsService
from app.services.opening_service import OpeningService
from app.services.llm_service import LLMService

from app.utils.metrics import (
    calculate_centipawn_loss,
    classify_move,
)

from app.utils.accuracy import calculate_accuracy


class GameAnalysisService:

    def __init__(self):
        self.stockfish = StockfishService()
        self.statistics = StatisticsService()
        self.opening = OpeningService()
        self.llm = LLMService()

    def analyze_game(self, path: str):

        with open(path) as pgn:
            game = chess.pgn.read_game(pgn)

        board = game.board()

        analysis = []

        move_number = 1

        detected_opening = None

        for move in game.mainline_moves():

            # -----------------------------
            # Position BEFORE the move
            # -----------------------------
            fen = board.fen()

            # Engine analysis
            engine_analysis = self.stockfish.analyze_fen(fen)

            # Evaluation before move
            evaluation_before = self.stockfish.evaluate_fen(fen)

            # -----------------------------
            # Play the move
            # -----------------------------
            board.push(move)

            # -----------------------------
            # Detect opening AFTER move
            # -----------------------------
            opening = self.opening.detect_opening(board.fen())

            if opening is not None:
                detected_opening = opening

            # Evaluation after move
            evaluation_after = self.stockfish.evaluate_fen(board.fen())

            # Centipawn loss
            cpl = calculate_centipawn_loss(
                evaluation_before,
                evaluation_after,
            )

            # Classification
            classification = classify_move(cpl)

            move_entry = {
                "move_number": move_number,
                "played_move": move.uci(),
                "fen": fen,
                "best_move": engine_analysis["best_move"],
                "evaluation_before": evaluation_before,
                "evaluation_after": evaluation_after,
                "centipawn_loss": cpl,
                "classification": classification,
            }

            # Best moves need no coaching explanation
            if classification != "Best":
                move_entry["explanation"] = self.llm.explain_move(move_entry)
            else:
                move_entry["explanation"] = None

            analysis.append(move_entry)

            move_number += 1

        # -----------------------------
        # Statistics
        # -----------------------------
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
            "opening": detected_opening,
            "statistics": statistics,
            "moves": analysis,
        }
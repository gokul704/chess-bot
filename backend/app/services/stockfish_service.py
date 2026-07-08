import chess
import chess.engine

from app.core.logging import logger
from app.core.constants import ENGINE_DEPTH, TOP_MOVES
from app.core.settings import settings


class StockfishService:
    def __init__(self):
        logger.info("Starting Stockfish engine...")
        self.engine = chess.engine.SimpleEngine.popen_uci(
            settings.STOCKFISH_PATH
        )

    def _format_score(self, score):
        """
        Convert Stockfish score into a structured response.
        """

        relative = score.relative

        if relative.is_mate():
            return {
                "type": "mate",
                "value": relative.mate(),
                "display": f"Mate in {relative.mate()}",
            }

        cp = relative.score()

        return {
            "type": "cp",
            "value": cp,
            "display": f"{cp / 100:+.2f}",
        }

    def analyze_fen(self, fen: str):

        logger.info("Analyzing position")

        board = chess.Board(fen)

        analysis = self.engine.analyse(
            board,
            chess.engine.Limit(depth=ENGINE_DEPTH),
            multipv=TOP_MOVES,
        )

        best = analysis[0]

        best_move = best["pv"][0].uci()

        top_moves = []

        for line in analysis:

            move = line["pv"][0].uci()

            score = self._format_score(line["score"])

            top_moves.append(
                {
                    "move": move,
                    "evaluation": score["display"],
                }
            )

        return {
            "best_move": best_move,
            "depth": ENGINE_DEPTH,
            "evaluation": self._format_score(best["score"]),
            "top_moves": top_moves,
        }

    def close(self):
        logger.info("Closing Stockfish engine")
        self.engine.quit()
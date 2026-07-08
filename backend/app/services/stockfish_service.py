import chess
import chess.engine


class StockfishService:
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(
            "/opt/homebrew/bin/stockfish"
        )

    def analyze_fen(self, fen: str):
        board = chess.Board(fen)

        result = self.engine.analyse(
            board,
            chess.engine.Limit(depth=18),
        )

        best_move = result["pv"][0]

        score = result["score"].relative

        return {
            "best_move": best_move.uci(),
            "evaluation": str(score),
        }

    def close(self):
        self.engine.quit()
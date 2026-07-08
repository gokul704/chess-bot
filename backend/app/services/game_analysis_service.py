import chess
import chess.pgn

from app.services.stockfish_service import StockfishService


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

            fen = board.fen()

            engine = self.stockfish.analyze_fen(fen)

            analysis.append(
                {
                    "move_number": move_number,
                    "played_move": move.uci(),
                    "fen": fen,
                    "best_move": engine["best_move"],
                    "evaluation": engine["evaluation"]["display"],
                }
            )

            board.push(move)

            move_number += 1

        return {
            "white": game.headers["White"],
            "black": game.headers["Black"],
            "result": game.headers["Result"],
            "moves": analysis,
        }
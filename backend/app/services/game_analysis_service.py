import chess.pgn


class GameAnalysisService:

    def load_game(self, path: str):
        with open(path) as pgn:
            game = chess.pgn.read_game(pgn)

        return {
            "white": game.headers["White"],
            "black": game.headers["Black"],
            "result": game.headers["Result"],
            "moves": len(list(game.mainline_moves()))
        }
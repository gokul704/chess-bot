import json
from pathlib import Path


class OpeningService:

    def __init__(self):

        path = (
            Path(__file__).parent.parent
            / "data"
            / "eco.json"
        )

        with open(path, "r", encoding="utf-8") as f:
            raw_openings = json.load(f)

        # ponytail: eco.json keys include halfmove clock + fullmove number,
        # so transposed move orders (same position, different counters) miss.
        # Index by position only (board + turn + castling + en passant).
        self.openings = {
            self._normalize(fen): data
            for fen, data in raw_openings.items()
        }

    def _normalize(self, fen: str) -> str:
        return " ".join(fen.split(" ")[:4])

    def detect_opening(self, fen: str):
        return self.openings.get(self._normalize(fen))
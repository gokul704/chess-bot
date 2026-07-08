from collections import Counter


class StatisticsService:
    """
    Generates game-level statistics from move analysis.
    """

    def calculate(self, moves: list) -> dict:

        # Count move classifications
        classifications = Counter(
            move["classification"] for move in moves
        )

        # Calculate average CPL
        total_cpl = sum(
            move["centipawn_loss"] for move in moves
        )

        total_moves = len(moves)

        average_cpl = (
            round(total_cpl / total_moves, 2)
            if total_moves > 0
            else 0
        )

        return {
            "best": classifications.get("Best", 0),
            "excellent": classifications.get("Excellent", 0),
            "good": classifications.get("Good", 0),
            "inaccuracy": classifications.get("Inaccuracy", 0),
            "mistake": classifications.get("Mistake", 0),
            "blunder": classifications.get("Blunder", 0),
            "total_moves": total_moves,
            "average_centipawn_loss": average_cpl,
        }
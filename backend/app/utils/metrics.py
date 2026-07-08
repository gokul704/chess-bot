def calculate_centipawn_loss(before: int, after: int) -> int:
    """
    Returns the absolute centipawn loss.
    """

    return abs(before - after)

def classify_move(cpl: int) -> str:

    if cpl <= 10:
        return "Best"

    if cpl <= 30:
        return "Excellent"

    if cpl <= 60:
        return "Good"

    if cpl <= 100:
        return "Inaccuracy"

    if cpl <= 300:
        return "Mistake"

    return "Blunder"


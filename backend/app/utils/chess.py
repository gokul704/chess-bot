def format_score(score):
    if score.is_mate():
        return f"Mate in {score.mate()}"

    cp = score.score()

    return f"{cp/100:+.2f}"
def calculate_accuracy(avg_cpl: float):

    accuracy = max(0, 100 - avg_cpl / 2)

    return round(accuracy, 1)
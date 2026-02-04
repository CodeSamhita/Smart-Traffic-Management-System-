WEIGHTS = {
    "motorcycle": 1,
    "car": 2,
    "bus": 3,
    "truck": 3,
    "person": 0.5   # pedestrians influence
}

def calculate_congestion(detections):
    """
    Input: list of detections in QUEUE zone
    Output: congestion score
    """
    score = 0
    for d in detections:
        score += WEIGHTS.get(d["class"], 1)
    return score

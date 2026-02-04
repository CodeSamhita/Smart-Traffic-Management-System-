def decide_signal(congestion_score, emergency=False):
    """
    Core decision logic
    """
    if emergency:
        return {
            "signal": "GREEN",
            "green_time": 60,
            "reason": "Emergency Vehicle Priority"
        }

    # Adaptive timing
    green_time = min(60, max(10, congestion_score * 2))

    return {
        "signal": "GREEN",
        "green_time": green_time,
        "reason": "Adaptive Congestion Control"
    }

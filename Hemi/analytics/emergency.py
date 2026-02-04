def detect_emergency(detections):
    """
    Simple logic:
    If ambulance class is detected → emergency
    (Later you can add siren/audio logic)
    """
    for d in detections:
        if d["class"] == "ambulance":
            return True
    return False

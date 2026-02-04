def classify_zone(y, frame_height):
    """
    Indian traffic: use vertical zones instead of lanes
    """
    if y < frame_height * 0.4:
        return "ENTRY"
    elif y < frame_height * 0.75:
        return "QUEUE"
    else:
        return "EXIT"

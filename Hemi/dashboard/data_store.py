congestion_history = []
emergency_count = 0

def add_congestion(value):
    congestion_history.append(value)

def add_emergency():
    global emergency_count
    emergency_count += 1

def get_data():
    return congestion_history, emergency_count

from vision.detector import detect_vehicles
from vision.zone_mapper import classify_zone
from analytics.congestion import calculate_congestion
from analytics.emergency import detect_emergency
from signal_control.optimizer import decide_signal
from simulation.simulator import simulate_signal
from dashboard.data_store import add_congestion, add_emergency

VIDEO_PATH = "assets/traffic_video.mp4"

if __name__ == "__main__":
    all_frames = detect_vehicles(VIDEO_PATH)

    for frame in all_frames:
        queue_zone_vehicles = []

        for d in frame:
            zone = classify_zone(d["center"][1], d["frame_height"])
            if zone == "QUEUE":
                queue_zone_vehicles.append(d)

        congestion = calculate_congestion(queue_zone_vehicles)
        emergency = detect_emergency(frame)

        add_congestion(congestion)
        if emergency:
            add_emergency()

        signal_decision = decide_signal(congestion, emergency)
        simulate_signal(signal_decision)

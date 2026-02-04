import time

def simulate_signal(signal_data):
    direction = "MAIN_ROAD"
    green_time = signal_data["green_time"]

    print("\n==============================")
    print(f" SIGNAL: {signal_data['signal']}")
    print(f" DIRECTION: {direction}")
    print(f" TIME: {green_time}s")
    print(f" REASON: {signal_data['reason']}")
    print("==============================")

    for i in range(green_time, 0, -1):
        print(f" Green ends in {i}s", end="\r")
        time.sleep(1)

    print("\nSignal cycle completed.\n")

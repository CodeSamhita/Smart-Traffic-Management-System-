# presenting a single lane intersection.



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------
# Simulation Parameters
# -----------------------------
ROAD_LENGTH = 1000        # meters
NUM_CARS = 20
MAX_SPEED = 15           # m/s (~54 km/h)
SAFE_DISTANCE = 20        # meters
DT = 0.2                 # time step (seconds)

# Traffic signal
SIGNAL_POSITION = 700
GREEN_TIME = 20
RED_TIME = 20

# -----------------------------
# Vehicle Initialization
# -----------------------------
positions = np.linspace(0, 300, NUM_CARS)
speeds = np.zeros(NUM_CARS)

# -----------------------------
# Traffic Signal Logic
# -----------------------------
def signal_state(t):
    cycle = GREEN_TIME + RED_TIME
    return "GREEN" if (t % cycle) < GREEN_TIME else "RED"

# -----------------------------
# Update Function
# -----------------------------
def update(frame):
    global positions, speeds

    time = frame * DT
    light = signal_state(time)

    for i in range(NUM_CARS):
        # Distance to next car
        if i < NUM_CARS - 1:
            gap = positions[i + 1] - positions[i]
        else:
            gap = ROAD_LENGTH

        # Distance to traffic light
        dist_to_light = SIGNAL_POSITION - positions[i]

        # Decide target speed
        target_speed = MAX_SPEED

        # Red light behavior
        if light == "RED" and 0 < dist_to_light < SAFE_DISTANCE * 1.5:
            target_speed = 0

        # Car-following rule
        if gap < SAFE_DISTANCE:
            target_speed = 0

        # Smooth acceleration / braking
        speeds[i] += 0.5 * (target_speed - speeds[i]) * DT
        speeds[i] = max(0, min(MAX_SPEED, speeds[i]))

    # Update positions
    positions += speeds * DT

    # Keep cars on road
    positions = np.clip(positions, 0, ROAD_LENGTH)

    # Update plot
    car_dots.set_offsets(np.c_[positions, np.zeros(NUM_CARS)])
    signal_dot.set_color("green" if light == "GREEN" else "red")
    title.set_text(f"Time: {time:.1f}s | Signal: {light}")

    return car_dots, signal_dot

# -----------------------------
# Visualization Setup
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 2))
ax.set_xlim(0, ROAD_LENGTH)
ax.set_ylim(-1, 1)
ax.set_yticks([])
ax.set_xlabel("Road Position (meters)")

# Cars
car_dots = ax.scatter(positions, np.zeros(NUM_CARS), s=50)

# Traffic signal
signal_dot = ax.scatter(SIGNAL_POSITION, 0, s=200, color="green")

title = ax.set_title("Smart Traffic Simulation")

# -----------------------------
# Run Animation
# -----------------------------
ani = FuncAnimation(
    fig,
    update,
    frames=500,
    interval=50,
    blit=True
)

plt.show()

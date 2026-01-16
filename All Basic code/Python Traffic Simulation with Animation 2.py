import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# =========================
# CONFIGURATION
# =========================
DT = 0.2
ROAD = 90
STOP_LINE = 10
MAX_SPEED = 8
SPAWN_RATE = 0.06

GREEN_TIME = 15
YELLOW_TIME = 4

DIRECTIONS = ["N", "S", "E", "W"]

# =========================
# SIGNAL CONTROLLER
# =========================
class SignalController:
    def __init__(self):
        self.index = 0
        self.state = "G"
        self.timer = 0

    def current_lane(self):
        return DIRECTIONS[self.index]

    def update(self):
        self.timer += DT

        if self.state == "G" and self.timer >= GREEN_TIME:
            self.state = "Y"
            self.timer = 0

        elif self.state == "Y" and self.timer >= YELLOW_TIME:
            self.state = "R"
            self.timer = 0

        elif self.state == "R":
            self.index = (self.index + 1) % 4
            self.state = "G"

    def lane_state(self, lane):
        if lane == self.current_lane():
            return self.state
        return "R"

# =========================
# VEHICLE
# =========================
class Vehicle:
    def __init__(self, direction):
        self.dir = direction
        self.speed = 0

        if direction == "N":
            self.x, self.y = 0, ROAD
        elif direction == "S":
            self.x, self.y = 0, -ROAD
        elif direction == "E":
            self.x, self.y = ROAD, 0
        else:
            self.x, self.y = -ROAD, 0

    def distance_to_stop(self):
        return abs(self.y) if self.dir in ["N", "S"] else abs(self.x)

    def update(self, signal):
        sig = signal.lane_state(self.dir)
        stop = sig in ["R", "Y"] and self.distance_to_stop() < STOP_LINE

        target = 0 if stop else MAX_SPEED
        self.speed += (target - self.speed) * 0.4
        self.speed = max(0, self.speed)

        if self.dir == "N":
            self.y -= self.speed * DT
        elif self.dir == "S":
            self.y += self.speed * DT
        elif self.dir == "E":
            self.x -= self.speed * DT
        else:
            self.x += self.speed * DT

    def out_of_bounds(self):
        return abs(self.x) > ROAD or abs(self.y) > ROAD

# =========================
# SIMULATION STATE
# =========================
signal = SignalController()
vehicles = []

def spawn_vehicle():
    if random.random() < SPAWN_RATE:
        vehicles.append(Vehicle(random.choice(DIRECTIONS)))

# =========================
# UPDATE LOOP
# =========================
def update(frame):
    signal.update()
    spawn_vehicle()

    xs, ys = [], []

    for v in vehicles[:]:
        v.update(signal)
        if v.out_of_bounds():
            vehicles.remove(v)
        else:
            xs.append(v.x)
            ys.append(v.y)

    scat.set_offsets(np.c_[xs, ys])
    status.set_text(
        f"GREEN: {signal.current_lane()} | STATE: {signal.state}"
    )

    lights["N"].set_color(color(signal.lane_state("N")))
    lights["S"].set_color(color(signal.lane_state("S")))
    lights["E"].set_color(color(signal.lane_state("E")))
    lights["W"].set_color(color(signal.lane_state("W")))

    return scat, status

def color(state):
    return {"G": "green", "Y": "yellow", "R": "red"}[state]

# =========================
# VISUALIZATION
# =========================
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-ROAD, ROAD)
ax.set_ylim(-ROAD, ROAD)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Single-Lane-At-A-Time Traffic Intersection")

# Roads
ax.plot([-ROAD, ROAD], [0, 0], linewidth=6)
ax.plot([0, 0], [-ROAD, ROAD], linewidth=6)

scat = ax.scatter([], [], s=30)

# Traffic lights
lights = {
    "N": ax.scatter(5, 15, s=200),
    "S": ax.scatter(-5, -15, s=200),
    "E": ax.scatter(15, -5, s=200),
    "W": ax.scatter(-15, 5, s=200),
}

status = ax.text(-80, 80, "", fontsize=10)

ani = FuncAnimation(fig, update, interval=50)
plt.show()

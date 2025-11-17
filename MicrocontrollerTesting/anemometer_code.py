import time
import board
from analogio import AnalogIn

analog_2in = AnalogIn(board.A2)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536


# Calibration / thresholds (tune these for your sensor)
CLOSED_THRESHOLD = 0.1   # voltage considered a "closed" reading
OPEN_THRESHOLD = 3.2     # voltage considered an "open" reading
DEBOUNCE_SEC = 0.05      # ignore additional triggers within 50 ms
CALIB_FACTOR = 0.66      # conversion from closures/sec -> m/s (device-specific)
AVG_WINDOW = 5           # seconds to average over


# State and measurement variables
closure_count = 0
wind_speeds = []  # stores recent wind speed readings (one per second)
last_closed = False
last_count_time = 0
start_time = time.monotonic()


while True:
    voltage = get_voltage(analog_2in)
    now = time.monotonic()

    # Use explicit hysteresis (open/closed) so intermediate voltages don't break edge detection.
    is_closed = voltage < CLOSED_THRESHOLD
    is_open = voltage > OPEN_THRESHOLD

    # Count a closure on the falling edge into the closed state, with debounce
    if is_closed and not last_closed:
        if now - last_count_time >= DEBOUNCE_SEC:
            closure_count += 1
            last_count_time = now
        last_closed = True
    elif is_open:
        # once clearly open, allow next falling edge to be counted
        last_closed = False

    # Every second, compute instant and averaged wind speed
    if now - start_time >= 1.0:
        closures_per_sec = closure_count
        instant_speed = CALIB_FACTOR * closures_per_sec

        wind_speeds.append(instant_speed)
        if len(wind_speeds) > AVG_WINDOW:
            wind_speeds.pop(0)

        avg_speed = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0.0

        print(f"Closures/sec: {closures_per_sec:2d} | Instant wind: {instant_speed:4.2f} m/s | Avg wind ({AVG_WINDOW}s): {avg_speed:4.2f} m/s", flush=True)

        # reset for next second
        closure_count = 0
        start_time = now

    # small delay to avoid busy-looping too tightly
    time.sleep(0.01)

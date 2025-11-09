import time
import board
from analogio import AnalogIn

analog_0in = AnalogIn(board.A0)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def check_status(voltage):
    if voltage > 3.2:
        return "open"
    elif voltage < 0.1:
        return "closed"
    else:
        return "???"

# Variables for counting closures per second
closure_count = 0
wind_speed = 0
wind_speeds = []  # stores recent wind speed readings
avg_window = 5    # number of seconds to average over
last_state = "open"
start_time = time.monotonic()

while True:
    voltage = get_voltage(analog_0in)
    state = check_status(voltage)

    # Detect a transition from open -> closed
    if state == "closed" and last_state == "open":
        closure_count += 1

    last_state = state

    # Every second, print the number of closures and reset the counter
    if time.monotonic() - start_time >= 1.0:
        wind_speed = 0.66 * closure_count
        wind_speeds.append(wind_speed)

        # Keep only the most recent avg_window readings
        if len(wind_speeds) > avg_window:
            wind_speeds.pop(0)

        avg_speed = sum(wind_speeds) / len(wind_speeds)

        print(f"Closures/sec: {closure_count:2d} | Instant wind: {wind_speed:4.2f} m/s | Avg wind ({avg_window}s): {avg_speed:4.2f} m/s")
        closure_count = 0
        start_time = time.monotonic()

    time.sleep(0.01)

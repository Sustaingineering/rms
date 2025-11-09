import time
import board
from analogio import AnalogIn


analog_0_in = AnalogIn(board.A0)
analog_1_in = AnalogIn(board.A1)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536


def check_status(voltage):
    if voltage > 3:
        return "active"
    else:
        return "inactive"

status = "open"
delay = 0
last_close = 0
last_open = time.monotonic()
time_since_close = 0
time_since_open = 0
rpm = 0
close_times = []
closes_per_rot = 12

while True:
    voltage_0 = get_voltage(analog_0_in)
    voltage_1 = get_voltage(analog_1_in)

    status_0 = check_status(voltage_0)
    status_1 = check_status(voltage_1)


    if status == "open" and status_1 == "active": # just closed
        status = "closed"
        if last_close == 0: last_close = time.monotonic()
        else: 
            current_time = time.monotonic()
            time_since_close = current_time - last_close
            last_close = current_time

            close_times.append(time_since_close)

            if len(close_times) > closes_per_rot:
                close_times.pop(0)

            total_time = sum(close_times) * closes_per_rot / len(close_times)

            rpm = 1 / (total_time) * 60


    if status == "closed" and status_0 == "active": # just opened
        status = "open"
        if last_open == 0: last_open = time.monotonic()
        else: 
            current_time = time.monotonic()
            time_since_open = current_time - last_open
            last_open = current_time



    # pin 0: {voltage_0:1.3f}, pin 1: {voltage_1:1.3f}, pin 0: {status_0:8s}, pin 1: {status_1:8s}, 
    print(f"status: {status:6s}, close time: {time_since_close:1.3f}, open time: {time_since_open:1.3f}, rpm: {rpm}")
    time.sleep(0.001)


    #pin 0 high = closed
    #pin 1 high = open
    #15 rps

"""
Sensors missing on March 7th 2026, and RMS system needs to be tested so this is code used 
that only tests on the lightgate (which is still connected to the turbine)
Previous code used is under main_no_temp.py
"""

#Microcontroller Imports
import board
import time
from analogio import AnalogIn

i2c = board.I2C()

analog_0_in = AnalogIn(board.A0)
analog_1_in = AnalogIn(board.A1)
analog_2in = AnalogIn(board.A2)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def check_status_lightGate(voltage):
    if voltage > 2.8:
        return "light"
    else:
        return "dark"
    
#Lightgate variables
SLITS_PER_REV = 2
GEAR_RATIO = 7
time_difference_dark_pass = 0
time_difference_light_pass = 0
half_rot_time = 5
last_status = "unknown"
begin_dark_time = 0
end_dark_time = 0
begin_light_time = 0
end_light_time = 0

while True:
    timestamp = time.monotonic()
    print(f"{timestamp:.3f},", end='')

    voltage_0 = get_voltage(analog_0_in)
    voltage_1 = get_voltage(analog_1_in)

    current_time = time.monotonic()
    status = check_status_lightGate(voltage_0)

    if status != last_status:
        if status == "dark":
            end_light_time = current_time
            begin_dark_time = current_time

            time_difference_light_pass = end_light_time - begin_light_time

            half_rot_time = time_difference_light_pass + time_difference_dark_pass
        if status == "light":
            begin_light_time = current_time
            end_dark_time = current_time

            time_difference_dark_pass = end_dark_time - begin_dark_time
        
        last_status = status
        full_rot_time = half_rot_time * 2
        rpm_gear = 60/full_rot_time
        rpm_turbine = rpm_gear / GEAR_RATIO

    print(f"{rpm_turbine:5.2f}", end=',')

    time.sleep(0.0001)
import time
import board
from analogio import AnalogIn

analog_2in = AnalogIn(board.A1)

def get_voltage(pin):
    return (pin.value * 5) / 65536

while True:
    voltage = get_voltage(analog_2in)

    # Since one parallel circuit right now, voltage halved
    # Voltage under get_voltage is * 5 since max voltage is 10V
    # However, microcontroller can only read a max of 3.3V, so another parallel circuit is needed to halve voltage to 2.5V [TO DO]
    # In its current state, voltage between 3.3V and 5V (originally 6.6V and 10V) is not read
    # So, max speed reading should be 30m/s but is instead 22m/s

    # convert 1000 V to mV and apply converstion
    curr_speed = voltage*1000*0.006

    print(f"Time: {time.monotonic():.1f} s | Voltage: {voltage:4.5f} V | Current speed: {curr_speed:4.5f} m/s")

    # small delay to avoid busy-looping too tightly
    time.sleep(1)

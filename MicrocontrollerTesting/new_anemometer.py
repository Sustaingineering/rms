import time
import board
from analogio import AnalogIn

analog_2in = AnalogIn(board.A1)

def get_voltage(pin):
  # max expected V is 2.5V  
    return (pin.value * 2.5) / 65536

while True:
    voltage = get_voltage(analog_2in)

    # convert 1000 V to mV and apply converstion (refer to PDF for calculation + wiring)
    curr_speed = voltage*1000*0.003*4

    print(f"Time: {time.monotonic():.1f} s | Stepped down voltage: {voltage*1000:4.2f} mV | Original voltage: {voltage*4*1000:4.2f} mV | Speed: {curr_speed:4.5f} m/s")

    # small delay to avoid busy-looping too tightly
    time.sleep(1)

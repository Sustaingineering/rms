import time
import board
from analogio import AnalogIn

# Initialize the analog pin connected to the sensor's AOUT
moisture_pin_1 = AnalogIn(board.A0)
moisture_pin_2 = AnalogIn(board.A2)

# --- CALIBRATION VALUES ---
# Step 1: Hold the sensor in the air and look at the printed value. Replace 50000 with your number.
AIR_VALUE = 50000  

# Step 2: Submerge the sensor in water up to the white line. Replace 20000 with your number.
WATER_VALUE = 20000  

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

while True:
    raw_value_1 = moisture_pin_1.value
    raw_value_2 = moisture_pin_2.value
    
    
    # Calculate percentage based on calibration points
    # Prevents values outside 0-100% bounds
    if raw_value_1 >= AIR_VALUE:
        percentage_1 = 0
    elif raw_value_1 <= WATER_VALUE:
        percentage_1 = 100
    else:
        percentage_1 = int((AIR_VALUE - raw_value_1) / (AIR_VALUE - WATER_VALUE) * 100)

    if raw_value_2 >= AIR_VALUE:
        percentage_2 = 0
    elif raw_value_2 <= WATER_VALUE:
        percentage_2 = 100
    else:
        percentage_2 = int((AIR_VALUE - raw_value_2) / (AIR_VALUE - WATER_VALUE) * 100)
        
    print(f"EK1940 Sensor 1: {raw_value_1} | Moisture: {percentage_1}%")
    print(f"EK1940 Sensor 2: {raw_value_2} | Moisture: {percentage_2}%")
    time.sleep(1)
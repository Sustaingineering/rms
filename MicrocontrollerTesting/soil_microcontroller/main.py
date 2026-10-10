import time
import board
from analogio import AnalogIn

# Initialize the analog pin connected to the sensor's AOUT
moisture_pin = AnalogIn(board.A0)

# --- CALIBRATION VALUES ---
# Step 1: Hold the sensor in the air and look at the printed value. Replace 50000 with your number.
AIR_VALUE = 50000  

# Step 2: Submerge the sensor in water up to the white line. Replace 20000 with your number.
WATER_VALUE = 20000  

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

while True:
    raw_value = moisture_pin.value
    
    # Calculate percentage based on calibration points
    # Prevents values outside 0-100% bounds
    if raw_value >= AIR_VALUE:
        percentage = 0
    elif raw_value <= WATER_VALUE:
        percentage = 100
    else:
        percentage = int((AIR_VALUE - raw_value) / (AIR_VALUE - WATER_VALUE) * 100)
        
    print(f"Raw Value: {raw_value} | Moisture: {percentage}%")
    time.sleep(1)

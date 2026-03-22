"""
This MC is currently being used for RMS testing - it is not part of the RMS network or connected to 
the turbine

The MC is only currently connected to:
- DPS310 (Temperature and Pressure)
- SHT45 (Humidity and Temperature)
"""

#Microcontroller Imports
import board
import time
from adafruit_dps310.basic import DPS310 #DPS310
import adafruit_sht4x #SHT45

#Board setup
i2c = board.I2C()
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

#DPS310
dps310 = DPS310(i2c)

#SHT45
sht = adafruit_sht4x.SHT4x(i2c)
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

while True:
    #SHT
    sht_temp, sht_humidity = sht.measurements

    #DPS
    dps_temp = dps310.temperature
    dps_pressure = dps310.pressure
    
    #Timestamp
    timestamp = time.monotonic() # Using monotonic() is often better for duration on MCUs

    print(f"{timestamp:.3f},{sht_temp:.2f},{sht_humidity:.2f},{dps_pressure:.2f}\n")
    
    time.sleep(1)
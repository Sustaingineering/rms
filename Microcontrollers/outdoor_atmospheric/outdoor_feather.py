import time
import board
from adafruit_dps310.basic import DPS310 #DPS310
import adafruit_sht4x #SHT45
from analogio import AnalogIn #pins for microcontroller

analog_2in = AnalogIn(board.A1)
i2c = board.I2C()

########## To Edit #####################
#True = Data read from sensor
#False = Data ignored from sensor 
print_anemometer = True
print_SHT45 = True
print_DPS310 = True

#DPS310
if print_DPS310 == True:
    dps310 = DPS310(i2c)

#SHT45
if print_SHT45 == True:
    sht = adafruit_sht4x.SHT4x(i2c)
    sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def get_anemometer_voltage(pin):
  # max expected V is 2.5V  
    return (pin.value * 2.5) / 65536

while True:
    #Timestamp
    timestamp = time.monotonic() # Using monotonic() is often better for duration on MCUs
    print(f"{timestamp:.3f},", end=' ')

    if print_anemometer:
        #anometer voltage reading
        voltage = get_anemometer_voltage(analog_2in)
        # convert 1000 V to mV and apply converstion (refer to PDF for calculation + wiring)
        curr_speed = voltage*1000*0.003*4

        print(f"Wind speed: {curr_speed:4.5f} m/s", end=' | ')

    #SHT45 Sensor
    if print_SHT45:
        sht_temp, sht_humidity = sht.measurements
        print(f"Temperature: {sht_temp:.2f}°C, Humidity: {sht_humidity:.2f}%", end=' | ')
    
    #DPS310 Sensor
    if print_DPS310:
        dps_pressure = dps310.pressure
        print(f"Pressure: {dps_pressure:.2f} hPa")

    print("")
    time.sleep(1)

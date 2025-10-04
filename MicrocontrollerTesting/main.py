#Microcontroller Imports
import board
import time
from adafruit_dps310.basic import DPS310 #DPS310
import adafruit_sht4x #SHT45
import adafruit_ina228 #INA228

#Board setup
i2c = board.I2C()
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

#DPS310
dps310 = DPS310(i2c)

#SHT45
sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

#INA228
ina228 = adafruit_ina228.INA228(i2c)

print("timestamp,sht_temp_C,sht_rh_pct,dps_temp_C,dps_press_hPa,ina_current_mA,ina_bus_V,ina_shunt_mV,ina_power_mW,ina_energy_J,ina_die_C")

while True:
    temperature, relative_humidity = sht.measurements
    print("\nSHT45 Measurements:")
    print(f"Temperature: {temperature:.1f}C")
    print(f"Humidity: {relative_humidity:.1f}%")
    print("----------------------------------------")

    print("\nDPS310 Measurements:")
    print("Temperature = %.2f *C" % dps310.temperature)
    print("Pressure = %.2f hPa" % dps310.pressure)
    print("----------------------------------------")

    print("\nINA 228 Measurements:")
    print(f"Current: {ina228.current:.2f} mA")
    print(f"Bus Voltage: {ina228.bus_voltage:.2f} V")
    print(f"Shunt Voltage: {ina228.shunt_voltage*1000:.2f} mV")
    print(f"Power: {ina228.power:.2f} mW")
    print(f"Energy: {ina228.energy:.2f} J")
    print(f"Temperature: {ina228.die_temperature:.2f} °C")
    print("----------------------------------------")

    timestamp = time.time()  # seconds since epoch
    sht_temp, sht_rh = sht.measurements
    dps_temp = dps310.temperature
    dps_press = dps310.pressure
    ina_current = ina228.current
    ina_bus = ina228.bus_voltage
    ina_shunt = ina228.shunt_voltage * 1000
    ina_power = ina228.power
    ina_energy = ina228.energy
    ina_die_temp = ina228.die_temperature

    print(f"{timestamp:.3f},{sht_temp:.2f},{sht_rh:.2f},{dps_temp:.2f},{dps_press:.2f},{ina_current:.2f},{ina_bus:.2f},{ina_shunt:.2f},{ina_power:.2f},{ina_energy:.2f},{ina_die_temp:.2f}")
    time.sleep(1.0)

""" 
Adafruit RP2040 Testing
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
print("Hello World")
while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
"""
import board
import digitalio
import time
from adafruit_dps310.basic import DPS310
from adafruit_display_text.bitmap_label import Label
from displayio import Group
from terminalio import FONT

#SHT45
import adafruit_sht4x

#INA228
import adafruit_ina228


print("Hello World")

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
dps310 = DPS310(i2c)

#SHT45 Code
sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

#INA228 Code
ina228 = adafruit_ina228.INA228(i2c)



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
    time.sleep(1.0)

""" 
Adafruit RP2040
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
print("Hello World")
while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
"""
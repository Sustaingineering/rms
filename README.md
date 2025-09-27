## Remote Monitoring System (RMS)
The RMS is intended to be a monitoring system that reads information from various sensors throughout the SMRT Project, sends it into a database and transfers it to a web application.

### Microcontroller
We use the Adafruit RP2040 Feather as our Microcontroller, and program it with the CircuitPython library

### Sensors
- DPS310 as a Temperature and Pressure Sensor
- INA228 as a Current, Voltage, and Power Sensor
- SHT45 as a Temperature and Humidity Sensor

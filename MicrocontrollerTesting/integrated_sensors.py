#Microcontroller Imports
import board
import time
import adafruit_ina228 #INA228
import adafruit_ahtx0 #AHTX0
from analogio import AnalogIn #pins for microcontroller

########## To Edit #####################
#True = Data read from sensor
#False = Data ignored from sensor 
print_INA228 = True
print_AHTX0 = True
print_lightGate = True
print_anemometer = False

closes_per_rot = 12 # How many times the lightgate sensor closes per rotation

#Board setup
i2c = board.I2C()
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

#INA228
ina228 = adafruit_ina228.INA228(i2c)

#AHTX0
ahtx0 = adafruit_ahtx0.AHTx0(i2c)

#set up pins
analog_0_in = AnalogIn(board.A0)
analog_1_in = AnalogIn(board.A1)
analog_2in = AnalogIn(board.A2)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def check_status_lightGate(voltage):
    if voltage > 3:
        return "active"
    else:
        return "inactive"

def check_status_anemometer(voltage):
    if voltage > 3.2:
        return "open"
    elif voltage < 0.1:
        return "closed"
    else:
        return "???"

#Light Gate variables
status = "open"
delay = 0
last_close = 0
last_open = time.monotonic()
time_since_close = 0
time_since_open = 0
rpm = 0
close_times = []

#Anemometer variables 
# Variables for counting closures per second
closure_count = 0
wind_speed = 0
wind_speeds = []  # stores recent wind speed readings
avg_window = 5    # number of seconds to average over
last_state = "open"
start_time = time.monotonic()
last_closure_count = 0
last_wind_speed = 0
last_avg_speed = 0

while True: #FOR CSV WRITING
    #Timestamp
    timestamp = time.monotonic() # Using monotonic() is often better for duration on MCUs
    print(f"{timestamp:.3f},", end=' ')

    #For light gate:
    voltage_0 = get_voltage(analog_0_in)
    voltage_1 = get_voltage(analog_1_in)

    status_0 = check_status_lightGate(voltage_0)
    status_1 = check_status_lightGate(voltage_1)

    #INA
    if print_INA228 == True:
        ina_current = f"{ina228.current:2.2f}"
        ina_bus = f"{ina228.bus_voltage:2.2f}"
    else:
        ina_current = False
        ina_bus = False
    print(f"{ina_current},{ina_bus}", end=',')

    #AM2301B Sensor
    if print_AHTX0:
        ahtx0_temp = f"{ahtx0.temperature:2.2f}"
    else:
        ahtx0_temp = False
    print(f"{ahtx0_temp}", end=',')
    
    #Light gate:
    if print_lightGate == True:
        if status == "open" and status_1 == "active": # just closed
            status = "closed"
            if last_close == 0: last_close = time.monotonic()
            else: 
                current_time = time.monotonic()
                time_since_close = current_time - last_close
                last_close = current_time

                close_times.append(time_since_close)

                if len(close_times) > closes_per_rot:
                    close_times.pop(0)

                total_time = sum(close_times) * closes_per_rot / len(close_times)

                rpm = 1 / (total_time) * 60

        if status == "closed" and status_0 == "active": # just opened
            status = "open"
            if last_open == 0: last_open = time.monotonic()
            else: 
                current_time = time.monotonic()
                time_since_open = current_time - last_open
                last_open = current_time
    else:
        rpm = False
    print(f"{rpm}", end=',')

    #anemometer:
    if print_anemometer == True:
        voltage = get_voltage(analog_2in)
        state = check_status_anemometer(voltage)

        # Detect a transition from open -> closed
        if state == "closed" and last_state == "open":
            closure_count += 1

        last_state = state

        # Every second, print the number of closures and reset the counter
        if time.monotonic() - start_time >= 1.0:
            wind_speed = 0.66 * closure_count
            wind_speeds.append(wind_speed)

            # Keep only the most recent avg_window readings
            if len(wind_speeds) > avg_window:
                wind_speeds.pop(0)

            avg_speed = sum(wind_speeds) / len(wind_speeds)

            last_closure_count = closure_count
            last_wind_speed = wind_speed
            last_avg_speed = f"{avg_speed:4.2f}"

            closure_count = 0
            start_time = time.monotonic()
    else:
        last_avg_speed = False
    print(f"{last_avg_speed}", end='')

    print(" ")
    time.sleep(0.001)
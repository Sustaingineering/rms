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
print_anemometer = True

wind_speed_factor = 0.66 

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
    if voltage > 2.8:
        return "light"
    else:
        return "dark"

def check_status_anemometer(voltage):
    if voltage > 3.2:
        return "open"
    elif voltage < 0.1:
        return "closed"
    else:
        return "???"

#Lightgate variables
SLITS_PER_REV = 2
GEAR_RATIO = 7
time_difference_dark_pass = 0
time_difference_light_pass = 0
half_rot_time = 0
last_status = "unknown"
begin_dark_time = 0
end_dark_time = 0
begin_light_time = 0
end_light_time = 0

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
    print(f"{timestamp:.3f},", end='')

    #INA
    if print_INA228 == True:
        ina_current = ina228.current
        ina_bus = ina228.bus_voltage
    else:
        ina_current = False
        ina_bus = False
    print(f"{ina_current:5.2f},{ina_bus:5.2f}", end=',')

    # The AM2301B Sensor impedes on the lightgate sensor, probably creates a bottleneck
    """#AM2301B Sensor
    if print_AHTX0:
        ahtx0_temp = ahtx0.temperature
    else:
        ahtx0_temp = False
    print(f"{ahtx0_temp:6.2f}", end=',')"""
    
    # Light gate detection logic:
    if print_lightGate == True: # Assuming this flag controls light gate processing
        voltage_0 = get_voltage(analog_0_in)
        voltage_1 = get_voltage(analog_1_in)

        #when lightgate is detecting something
        #voltage_0 is 0.86
        #voltage_1 is 2.88
    
        #when lightgate is detecting nothing
        #voltage_0 is 2.86
        #voltage_1 is 0.97

        current_time = time.monotonic()

        status = check_status_lightGate(voltage_0)

        if status != last_status:

            if status == "dark":
                end_light_time = current_time
                begin_dark_time = current_time

                time_difference_light_pass = end_light_time - begin_light_time

                half_rot_time = time_difference_light_pass + time_difference_dark_pass
            if status == "light":
                begin_light_time = current_time
                end_dark_time = current_time

                time_difference_dark_pass = end_dark_time - begin_dark_time
            
            last_status = status

        full_rot_time = half_rot_time * 2
        rpm_gear = 60/full_rot_time
        rpm_turbine = rpm_gear / GEAR_RATIO
    print(f"{rpm_turbine:5.2f}", end=',')
        

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
            wind_speed = wind_speed_factor * closure_count
            wind_speeds.append(wind_speed)

            # Keep only the most recent avg_window readings
            if len(wind_speeds) > avg_window:
                wind_speeds.pop(0)

            avg_speed = sum(wind_speeds) / len(wind_speeds)

            last_closure_count = closure_count
            last_wind_speed = wind_speed
            last_avg_speed = avg_speed

            closure_count = 0
            start_time = time.monotonic()
    else:
        last_avg_speed = False
    print(f"{last_avg_speed:5.2f}", end='')

    print(" ")
    time.sleep(0.0001)
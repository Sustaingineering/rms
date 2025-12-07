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
SLITS_PER_REV = 2
GEAR_RATIO = 7

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

    #For light gate:
    voltage_0 = get_voltage(analog_0_in)
    voltage_1 = get_voltage(analog_1_in)

    status_0 = check_status_lightGate(voltage_0)
    status_1 = check_status_lightGate(voltage_1)

    #INA
    if print_INA228 == True:
        ina_current = ina228.current
        ina_bus = ina228.bus_voltage
    else:
        ina_current = False
        ina_bus = False
    print(f"{ina_current:5.2f},{ina_bus:5.2f}", end=',')

    #AM2301B Sensor
    if print_AHTX0:
        ahtx0_temp = ahtx0.temperature
    else:
        ahtx0_temp = False
    print(f"{ahtx0_temp:6.2f}", end=',')
    
    #Light gate:
    # Light gate:
    # Light Gate variables (Initial setup, retaining necessary state variables)
    status = "open"
    last_close = 1 # Time of the previous slit detection
    time_for_half_rev_shaft = 0 # Stores the calculated time (in seconds)
    
    # Inside your main 'while True:' loop:
    
    # Light gate detection logic:
    if print_lightGate == True: # Assuming this flag controls light gate processing
        # Check if the light gate just closed (meaning a slit was just detected)
        if status == "open" and status_1 == "active":
            status = "closed"
            
            current_time = time.monotonic()
            
            # This logic requires at least one previous reading (last_close != 0)
            if last_close != 0: 
                # Calculate the time elapsed since the last slit detection
                time_for_half_rev_shaft = current_time - last_close
                
                # *** At this point, 'time_for_half_rev_shaft' is the time
                # *** taken for the geared shaft to complete half a revolution.
                
                # You can now use this variable to calculate RPM:
                # Time for full rev (T) = time_for_half_rev_shaft * 2
                # RPM_shaft = 60 / T
                # RPM_turbine = RPM_shaft / 7
            
            last_close = current_time # Update the time of this most recent closure
    #print("Hello")
    #print(f"{current_time}")
    print(f"{time_for_half_rev_shaft:5.2f}", end='')
        

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
    time.sleep(0.001)
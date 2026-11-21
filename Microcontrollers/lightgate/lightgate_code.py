#Microcontroller Imports
import board
import time
import adafruit_ina228 #INA228
import adafruit_ahtx0 #AHTX0
from analogio import AnalogIn #pins for microcontroller

#Board setup
i2c = board.I2C()

#INA228
ina228 = adafruit_ina228.INA228(i2c)

#AHTX0
ahtx0 = adafruit_ahtx0.AHTx0(i2c)

#set up pins
analog_0_in = AnalogIn(board.A0)
analog_1_in = AnalogIn(board.A1)
analog_2_in = AnalogIn(board.A2)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def check_status_lightGate(voltage):
    if voltage > 2.8:
        return "light"
    else:
        return "dark"


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

while True: #FOR CSV WRITING
    #For light gate:
    voltage_0 = get_voltage(analog_0_in)
    voltage_1 = get_voltage(analog_1_in)

    #when lightgate is detecting something
    #voltage_0 is 0.86
    #voltage_1 is 2.88

    #when lightgate is detecting nothing
    #voltage_0 is 2.86
    #voltage_1 is 0.97

    status = check_status_lightGate(voltage_0)

    #print(status)

    current_time = time.monotonic() # Use monotonic consistently 

    #print(status)

    if status != last_status:

        if status == "dark": #the state just changed from light to dark
            end_light_time = current_time
            begin_dark_time = current_time
            
            time_difference_light_pass = end_light_time - begin_light_time

            half_rot_time = time_difference_light_pass + time_difference_dark_pass
            #print(half_rot_time)
            #print(time_difference_light_pass)

        if status == "light": #state changed from dark to light
            begin_light_time = current_time
            end_dark_time = current_time

            time_difference_dark_pass = end_dark_time - begin_dark_time
            #print(time_difference_dark_pass)
        
        last_status = status

    full_rot_time = half_rot_time * 2
    rpm_gear = 60/full_rot_time
    #print(rpm_gear)
    rpm_turbine = rpm_gear / GEAR_RATIO
    print(rpm_turbine)

    #print(" ")
    time.sleep(0.0001)

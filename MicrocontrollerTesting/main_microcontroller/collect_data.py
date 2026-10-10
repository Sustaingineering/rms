import serial
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

#Config
SERIAL_PORT       = '/dev/ttyACM0' #/dev/tty.usbmodem1101
BAUD_RATE         = 115200
MQTT_BROKER       = "io.adafruit.com"
ADAFRUIT_USERNAME = "SustaingineeringElec"
ADAFRUIT_KEY      = os.getenv('ADAFRUIT_KEY')
PUBLISH_INTERVAL  = 10 #seconds

#Client Setup
client = mqtt.Client()
client.username_pw_set(ADAFRUIT_USERNAME, ADAFRUIT_KEY)

print("Connecting...")
rc = client.connect(MQTT_BROKER, 1883, 60)
print("connect() returned:", rc == 0)

client.loop_start()

def clean_and_send(data_string):
    #Parses timestamp, temperature (sht), relative humidity, pressure and sends to MQTT
    try:
        data_parts = data_string.strip().split(",")
        temperature = data_parts[1]
        relative_humidity = data_parts[2]
        pressure = data_parts[3]
       # wind_speed = data_parts[3]

        print("Connected:", client.is_connected())

        r1 = client.publish(f"{ADAFRUIT_USERNAME}/feeds/temperature-sht45", temperature)
        r2 = client.publish(f"{ADAFRUIT_USERNAME}/feeds/rh-sht45", relative_humidity)
        r3 = client.publish(f"{ADAFRUIT_USERNAME}/feeds/pressure-dps310", pressure)
        #r4 = client.publish(f"{ADAFRUIT_USERNAME}/feeds/wind-speed", wind_speed)


        print(f"Publishing result: {r1.rc}, {r2.rc}, {r3.rc}") # 0 means publication is successful
        print(f"Sent: Temp: {temperature}, Hum: {relative_humidity}, Press: {pressure}")
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")

#Main Loop
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
    last_send = 0
    while True:
        line = ser.readline().decode('utf-8')

        if line and (time.monotonic() - last_send) > PUBLISH_INTERVAL:
            clean_and_send(line)
            last_send = time.monotonic()

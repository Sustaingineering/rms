import serial
import time
import paho.mqtt.client as mqtt

#Config
SERIAL_PORT       = '/dev/ttyACM0' #'/dev/tty.usbmodem1101'
BAUD_RATE         = 115200
MQTT_BROKER       = "io.adafruit.com"
ADAFRUIT_USERNAME = "SustaingineeringElec"
ADAFRUIT_KEY      = ""
PUBLISH_INTERVAL  = 30 #seconds

#Client Setup
client = mqtt.Client()
client.username_pw_set(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
client.connect(MQTT_BROKER, 1883, 60) #TCP port 1883 for unencrypted communication, 60s keepalive interval
client.loop_start()

def clean_and_send(data_string):
    #Parses timestamp, temperature (sht), relative humidity, pressure and sends to MQTT
    try:
        data_parts = data_string.strip().split(",")
        temperature = data_parts[1]
        relative_humidity = data_parts[2]
        pressure = data_parts[3]

        client.publish(f"{ADAFRUIT_USERNAME}/feeds/temperature-sht45", temperature)
        client.publish(f"{ADAFRUIT_USERNAME}/feeds/rh-sht45", relative_humidity)
        client.publish(f"{ADAFRUIT_USERNAME}/feeds/pressure-dps310", pressure)

        print(f"Sent: Temp: {temperature}, Hum: {relative_humidity}, Press: {pressure}")
    except:
        print("Error Occurred")

#Main Loop
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
    last_send = 0
    while True:
        line = ser.readline().decode('utf-8')

        if line and (time.monotonic() - last_send) > PUBLISH_INTERVAL:
            clean_and_send(line)
            last_send = time.monotonic()

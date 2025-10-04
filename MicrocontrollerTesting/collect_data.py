import serial
import pandas as pd
import time

# Adjust this to your Feather’s serial device
SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 115200     # Match whatever CircuitPython is using (default is 115200)

# Open the serial connection
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

# Read the header from the Feather
header_line = ser.readline().decode("utf-8").strip()
columns = header_line.split(",")

print("Columns detected:", columns)

# Create empty DataFrame
df = pd.DataFrame(columns=columns)

try:
    while True:
        line = ser.readline().decode("utf-8").strip()
        if not line:
            continue

        parts = line.split(",")
        if len(parts) != len(columns):
            print("Skipping malformed line:", line)
            continue

        # Convert to floats
        data = [float(x) for x in parts]
        df.loc[len(df)] = data

        print(df.tail(1))  # Show the latest reading

        # Optional: save to CSV every N samples
        if len(df) % 100 == 0:
            df.to_csv("sensor_data.csv", index=False)

except KeyboardInterrupt:
    print("Stopping logging...")

finally:
    # Final save
    df.to_csv("sensor_data_final.csv", index=False)
    ser.close()
import serial
import csv
import time

# --- Configuration ---
SERIAL_PORT = '/dev/tty.usbmodem1101' 
BAUD_RATE = 115200
OUTPUT_FILE = 'sensor_data.csv'

########## To Edit #####################
#True = Data read from sensor
#False = Data ignored from sensor 
print_INA228 = True
print_AHTX0 = True
print_lightGate = True
print_anemometer = True

frequency = 20 # frequency (smaller value = faster collection rate)

print(f"Attempting to connect to {SERIAL_PORT}...")

count = 0

try:
    # Connect to the serial port
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    print(f"Successfully connected to {SERIAL_PORT}.")
    time.sleep(2) # Wait for the connection to establish and MCU to reset

    # Header
    header = "timestamp,ina_current,ina_voltage,axtx0_temp,rpm,lg_avg_speed"
    header = header.split(',')

    # Determining whether the actual CSV file exists
    try: # Attempt to open CSV file
        with open(OUTPUT_FILE, 'r', newline='') as csv_file: 
            print("CSV file found")
            reader = csv.reader(csv_file)
    except: #If fails, create the file with name OUTPUT_FILE
        print("CSV file not found. Creating CSV ile")
        with open(OUTPUT_FILE, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

    # Determining if file has already been written to
    header_exists = False

    with open(OUTPUT_FILE, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)

        first_row = str(next(csv_file, None))
        
        if first_row == "timestamp,ina_current,ina_voltage,axtx0_temp,rpm,lg_avg_speed\r\n":
            header_exists = True
        else:
            header_exists = False
        
    
    if header_exists == True:
        print("Appending Data")
        with open(OUTPUT_FILE, 'a', newline = '') as csv_file:
            csv_writer = csv.writer(csv_file)

            while True:
                try:
                    count += 1
                    #print(count)
                    # Read one line of data from the serial port
                    data_line = ser.readline().decode('utf-8').strip()
                
                    # Check if the line is not empty
                    if data_line:
                        # Split the comma-separated string into a list
                        data_values = data_line.split(',')
                        if (count % frequency) == 0:
                            csv_writer.writerow(data_values)
                            print(f"Saving: {data_line}")
                        

                except UnicodeDecodeError:
                    print("Warning: Could not decode a line. Skipping.")
                except KeyboardInterrupt:
                    print("\nStopping logging.")
                    break

    else: #Header does not exist, CSV file is blank
        print("Header does not exist, writing new data")
        with open(OUTPUT_FILE, 'w', newline = '') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)

            while True:
                try:
                    count += 1
                    #print(count)
                    # Read one line of data from the serial port
                    data_line = ser.readline().decode('utf-8').strip()
                
                    # Check if the line is not empty
                    if data_line:
                        # Split the comma-separated string into a list
                        data_values = data_line.split(',')
                        if (count % frequency) == 0:
                            csv_writer.writerow(data_values)
                            print(f"Saving: {data_line}")

                except UnicodeDecodeError:
                    print("Warning: Could not decode a line. Skipping.")
                except KeyboardInterrupt:
                    print("\nStopping logging.")
                    break
        
except serial.SerialException as e:
    print(f"Error: Could not open serial port {SERIAL_PORT}.")
    print(f"Details: {e}")
    print("Please check the port name and ensure the device is connected.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
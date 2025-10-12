import serial
import csv
import time

# --- Configuration ---
SERIAL_PORT = '/dev/ttyACM0' 
BAUD_RATE = 115200
OUTPUT_FILE = 'sensor_data.csv'

print(f"Attempting to connect to {SERIAL_PORT}...")

try:
    # Connect to the serial port
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    print(f"Successfully connected to {SERIAL_PORT}.")
    time.sleep(2) # Wait for the connection to establish and MCU to reset

    # Header
    header = "timestamp,sht_temp_C,sht_rh_pct,dps_temp_C,dps_press_hPa,ina_current_mA,ina_bus_V,ina_shunt_mV,ina_power_mW,ina_energy_J,ina_die_C"
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
        
        if first_row == "timestamp,sht_temp_C,sht_rh_pct,dps_temp_C,dps_press_hPa,ina_current_mA,ina_bus_V,ina_shunt_mV,ina_power_mW,ina_energy_J,ina_die_C\r\n":
            header_exists = True
        else:
            header_exists = False
        
    
    if header_exists == True:
        print("Appending Data")
        with open(OUTPUT_FILE, 'a', newline = '') as csv_file:
            csv_writer = csv.writer(csv_file)

            while True:
                try:
                    # Read one line of data from the serial port
                    data_line = ser.readline().decode('utf-8').strip()

                    # Check if the line is not empty
                    if data_line:
                        print(f"Received: {data_line}")
                        # Split the comma-separated string into a list
                        data_values = data_line.split(',')
                        # Write the list as a new row in the CSV file
                        csv_writer.writerow(data_values)

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
                    # Read one line of data from the serial port
                    data_line = ser.readline().decode('utf-8').strip()

                    # Check if the line is not empty
                    if data_line:
                        print(f"Received: {data_line}")
                        # Split the comma-separated string into a list
                        data_values = data_line.split(',')
                        # Write the list as a new row in the CSV file
                        csv_writer.writerow(data_values)

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
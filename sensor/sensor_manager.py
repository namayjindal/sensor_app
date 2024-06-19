import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import csv
import os

class SensorManager:
    def __init__(self):
        self.buffers = {1: "", 2: "", 3: "", 4: ""}
        self.start_times = {1: None, 2: None, 3: None, 4: None}
        self.sensor_data = {
            1: {"timestamp": None, "values": [None] * 6},
            2: {"timestamp": None, "values": [None] * 6},
            3: {"timestamp": None, "values": [None] * 6},
            4: {"timestamp": None, "values": [None] * 6}
        }
        self.csv_filename = None
        self.lock = asyncio.Lock()
        self.devices = []

    async def notification_handler(self, sender, data, sensor_id):
        if self.start_times[sensor_id] is None:
            self.start_times[sensor_id] = datetime.now()  # Initialize start_time when the first data is received

        self.buffers[sensor_id] += data.decode('utf-8')
        buffer = self.buffers[sensor_id]

        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            self.buffers[sensor_id] = buffer

            # Skip empty lines
            if line.strip() == "":
                continue

            # Compute the elapsed time here inside the loop
            elapsed_time = (datetime.now() - self.start_times[sensor_id]).total_seconds() * 1000
            imu_values = list(map(float, line.split(',')))

            # Update the sensor_data dictionary
            self.sensor_data[sensor_id]["timestamp"] = elapsed_time
            self.sensor_data[sensor_id]["values"] = imu_values

            # Write to CSV file only when all sensors have data
            if all(self.sensor_data[i]["values"][0] is not None for i in range(1, 5)):
                timestamp = round(self.sensor_data[1]["timestamp"], 3)

                print(f"Right hand raw data: {self.sensor_data[1]['values']}")
                print(f"Left hand raw data: {self.sensor_data[2]['values']}")
                print(f"Right leg raw data: {self.sensor_data[3]['values']}")
                print(f"Left leg raw data: {self.sensor_data[4]['values']}")

                async with self.lock:
                    with open(self.csv_filename, 'a', newline='') as file:
                        writer = csv.writer(file)
                        row = [timestamp] + self.sensor_data[1]["values"] + self.sensor_data[2]["values"] + self.sensor_data[3]["values"] + self.sensor_data[4]["values"]
                        writer.writerow(row)

                # Reset sensor_data after writing to CSV
                for i in range(1, 5):
                    self.sensor_data[i]["timestamp"] = None
                    self.sensor_data[i]["values"] = [None] * 6

    async def connect_to_sensor(self, device, sensor_id, char_uuid):
        async with BleakClient(device) as client:
            if client.is_connected:
                print(f"Connected to {device.name}")

                await client.start_notify(char_uuid, lambda sender, data: asyncio.create_task(self.notification_handler(sender, data, sensor_id)))

                while True:
                    await asyncio.sleep(0.1)  # Adjust this sleep interval as needed
            else:
                print(f"Failed to connect to {device.name}")

    async def scan_devices(self):
        print("Scanning for devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"Device found: {device.name}, Address: {device.address}")
        self.devices = devices

    def filter_devices(self, target_names):
        self.devices = [d for d in self.devices if d.name in target_names]

    def set_csv_filename(self, filename):
        self.csv_filename = filename
        with open(self.csv_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp',
                             'right_hand_Accel_X', 'right_hand_Accel_Y', 'right_hand_Accel_Z', 'right_hand_Gyro_X', 'right_hand_Gyro_Y', 'right_hand_Gyro_Z',
                             'left_hand_Accel_X', 'left_hand_Accel_Y', 'left_hand_Accel_Z', 'left_hand_Gyro_X', 'left_hand_Gyro_Y', 'left_hand_Gyro_Z',
                             'right_leg_Accel_X', 'right_leg_Accel_Y', 'right_leg_Accel_Z', 'right_leg_Gyro_X', 'right_leg_Gyro_Y', 'right_leg_Gyro_Z',
                             'left_leg_Accel_X', 'left_leg_Accel_Y', 'left_leg_Accel_Z', 'left_leg_Gyro_X', 'left_leg_Gyro_Y', 'left_leg_Gyro_Z'])



    async def stop_tracking(self, label):
        self.is_tracking = False
        # Add label to JSON file

    def discard_data(self):
        if os.path.exists(self.csv_filename):
            os.remove(self.csv_filename)

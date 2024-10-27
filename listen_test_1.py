#!/usr/bin/env python3

import sys
import time
import socket
import json
import pandas as pd

# Define the IP and port to send data to
UNITY_IP = '172.30.224.1'  # Replace with Unity computer's IP address if different
UNITY_PORT = 5005           # Ensure this matches the port your Unity script is listening on
df = pd.read_csv("test7.csv")  # TODO: update

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main():
    try:
        print("Test listener is starting...")

        # Test data to send
        test_data = {
            'geolocation_sensor_0': {},
            'geolocation_sensor_1': {},
            'steering': {
                'steeringWheelAngle': 15.0,
                'roadWheelAngle': 10.0
            },
            'angle_reading': 5.0
        }

        for idx, row in df.iterrows():
            test_data['geolocation_sensor_0']['latitude'] = row['latitude truck']
            test_data['geolocation_sensor_0']['longitude'] = row['longitude truck']
            test_data['geolocation_sensor_0']['heading'] = row['heading truck']

            test_data['geolocation_sensor_1']['latitude'] = row['latitude trailer']
            test_data['geolocation_sensor_1']['longitude'] = row['longitude trailer']
            test_data['geolocation_sensor_1']['heading'] = row['heading trailer']

            test_data['steering']['steeringWheelAngle'] += 0.5
            test_data['steering']['roadWheelAngle'] += 0.3
            if test_data['steering']['steeringWheelAngle'] > 30.0:
                test_data['steering']['steeringWheelAngle'] = -30.0
            if test_data['steering']['roadWheelAngle'] > 20.0:
                test_data['steering']['roadWheelAngle'] = -20.0

            test_data['angle_reading'] = row['angle sensor']

            print(f"Sending test data: {json.dumps(test_data, indent=2)}")
            json_data = json.dumps(test_data)
            sock.sendto(json_data.encode('utf-8'), (UNITY_IP, UNITY_PORT))
            time.sleep(0.05)

    except Exception as e:
        print(f"An error occurred in listener_test: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Test listener stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()


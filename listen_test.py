#!/usr/bin/env python3

import sys
import time
import socket
import json

# Define the IP and port to send data to
UNITY_IP = '172.30.224.1'  # Replace with Unity computer's IP address if different
UNITY_PORT = 5005       # Ensure this matches the port your Unity script is listening on

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main():
    try:
        print("Test listener is starting...")

        # Test data to send
        test_data = {
            'geolocation_sensor_0': {
                'latitude': 57.718720,
                'longitude': 11.958876,
                'heading': 40.0
            },
            'geolocation_sensor_1': {
                'latitude': 57.718720,
                'longitude': 11.958876,
                'heading': 40.0
            },
            'steering': {
                'steeringWheelAngle': 15.0,
                'roadWheelAngle': 10.0
            },
            'angle_reading': 5.0
        }

        while True:
            # Optional: Modify the test data here to simulate changing values
            test_data['geolocation_sensor_0']['latitude'] += 0.0000001
            test_data['geolocation_sensor_0']['longitude'] += 0.0000001
            test_data['geolocation_sensor_0']['heading'] += 1.0
            if test_data['geolocation_sensor_0']['heading'] >= 360.0:
                test_data['geolocation_sensor_0']['heading'] -= 360.0

            test_data['geolocation_sensor_1']['latitude'] -= 0.00000001
            test_data['geolocation_sensor_1']['longitude'] -= 0.0000001
            test_data['geolocation_sensor_1']['heading'] -= 1.0
            if test_data['geolocation_sensor_1']['heading'] < 0.0:
                test_data['geolocation_sensor_1']['heading'] += 360.0

            test_data['steering']['steeringWheelAngle'] += 0.5
            test_data['steering']['roadWheelAngle'] += 0.3
            if test_data['steering']['steeringWheelAngle'] > 30.0:
                test_data['steering']['steeringWheelAngle'] = -30.0
            if test_data['steering']['roadWheelAngle'] > 20.0:
                test_data['steering']['roadWheelAngle'] = -20.0

            test_data['angle_reading'] += 0.2
            if test_data['angle_reading'] > 10.0:
                test_data['angle_reading'] = -10.0

            # Print the test data being sent
            print(f"Sending test data: {json.dumps(test_data, indent=2)}")

            # Serialize data to JSON
            json_data = json.dumps(test_data)

            # Send data over UDP
            sock.sendto(json_data.encode('utf-8'), (UNITY_IP, UNITY_PORT))

            time.sleep(0.05)  # Match the rate in your Unity script

    except Exception as e:
        print(f"An error occurred in listener_test: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Test listener stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()


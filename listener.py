#!/usr/bin/env python3

# Import necessary modules
import sys
import time
from OD4Session import OD4Session
import opendlv_standard_message_set_v0_9_10_pb2
import socket
import json

# Variables to store the latest values for each message type and sensor
latest_longitude_sensor_0 = None
latest_latitude_sensor_0 = None
latest_heading_sensor_0 = None

latest_longitude_sensor_1 = None
latest_latitude_sensor_1 = None
latest_heading_sensor_1 = None

latest_steeringWheelAngle = None
latest_roadWheelAngle = None

latest_angle_reading = None

# Define the IP and port to send data to
UNITY_IP = '172.30.224.1'  # Replace with Unity computer's IP address
UNITY_PORT = 5005          # You can choose any available port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Callback function to handle received Geolocation messages
def onGeolocation(msg, senderStamp, timeStamps):
    # Extract longitude, latitude, and heading
    longitude = msg.longitude
    latitude = msg.latitude
    heading = msg.heading

    global latest_longitude_sensor_0, latest_latitude_sensor_0, latest_heading_sensor_0
    global latest_longitude_sensor_1, latest_latitude_sensor_1, latest_heading_sensor_1

    if senderStamp == 0:  # Assuming '0' refers to sensor opendlv-device-gps-ncom-0
        latest_longitude_sensor_0 = longitude
        latest_latitude_sensor_0 = latitude
        latest_heading_sensor_0 = heading
    elif senderStamp == 1:  # Assuming '1' refers to sensor opendlv-device-gps-ncom-1
        latest_longitude_sensor_1 = longitude
        latest_latitude_sensor_1 = latitude
        latest_heading_sensor_1 = heading
    else:
        print(f"Unknown sensor with senderStamp={senderStamp}")

# Callback function to handle received Steering messages
def onSteering(msg, senderStamp, timeStamps):
    # Extract steering attributes
    steeringWheelAngle = msg.steeringWheelAngle
    roadWheelAngle = msg.roadWheelAngle

    global latest_steeringWheelAngle, latest_roadWheelAngle
    latest_steeringWheelAngle = steeringWheelAngle
    latest_roadWheelAngle = roadWheelAngle

# Callback function to handle received AngleReading messages
def onAngleReading(msg, senderStamp, timeStamps):
    # Extract angle
    angle = msg.angle

    global latest_angle_reading
    latest_angle_reading = angle

def main():
    try:
        print("Listener script is starting...")

        # Specify the CID (Communication ID) used by your OD4 session.
        cid = 100  # Replace with your actual CID if different

        # Create an OD4Session instance.
        session = OD4Session(cid)

        # Message IDs
        messageIDGeolocation = 1116  # opendlv.logic.sensation.Geolocation
        messageIDSteering = 199      # opendlv.proxy.rhino.Steering
        messageIDAngleReading = 1038 # opendlv.proxy.AngleReading

        # Register callback for the Geolocation message
        session.registerMessageCallback(
            messageIDGeolocation,
            onGeolocation,
            opendlv_standard_message_set_v0_9_10_pb2.opendlv_logic_sensation_Geolocation
        )

        # Register callback for the Steering message
        session.registerMessageCallback(
            messageIDSteering,
            onSteering,
            opendlv_standard_message_set_v0_9_10_pb2.opendlv_proxy_rhino_Steering
        )

        # Register callback for the AngleReading message
        session.registerMessageCallback(
            messageIDAngleReading,
            onAngleReading,
            opendlv_standard_message_set_v0_9_10_pb2.opendlv_proxy_AngleReading
        )

        # Connect to the network session.
        session.connect()
        print("Listener connected to OD4 session.")

        print("Listener started. Waiting for messages...")

        while True:
            time.sleep(0.05)  # Match the rate in your Unity coroutine

            data = {
                'geolocation_sensor_0': {
                    'latitude': latest_latitude_sensor_0,
                    'longitude': latest_longitude_sensor_0,
                    'heading': latest_heading_sensor_0
                },
                'geolocation_sensor_1': {
                    'latitude': latest_latitude_sensor_1,
                    'longitude': latest_longitude_sensor_1,
                    'heading': latest_heading_sensor_1
                },
                'steering': {
                    'steeringWheelAngle': latest_steeringWheelAngle,
                    'roadWheelAngle': latest_roadWheelAngle
                },
                'angle_reading': latest_angle_reading
            }

            # Optional: Print the latest data for debugging
            print(f"Latest data: {json.dumps(data, indent=2)}")

            # Serialize data to JSON
            json_data = json.dumps(data)

            # Send data over UDP
            sock.sendto(json_data.encode('utf-8'), (UNITY_IP, UNITY_PORT))

    except Exception as e:
        print(f"An error occurred in listener: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Listener stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()


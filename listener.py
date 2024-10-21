#!/usr/bin/env python3

# Import necessary modules
import sys
import time
from OD4Session import OD4Session
import opendlv_standard_message_set_v0_9_10_pb2
import socket
import json

# Variables to store the latest values for the two sensors
latest_longitude_sensor_0 = None
latest_latitude_sensor_0 = None
latest_longitude_sensor_1 = None
latest_latitude_sensor_1 = None
latest_steering_angle = None
latest_angle_reading = None

# Define the IP and port to send data to
UNITY_IP = '10.9.180.200'  # Replace with Unity computer's IP
UNITY_PORT = 5005  # You can choose any available port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Callback function to handle received Geolocation messages
def onGeolocation(msg, senderStamp, timeStamps):
    # Extract longitude and identify which sensor sent the message
    longitude = msg.longitude
    latitude = msg.latitude

    global latest_longitude_sensor_0, latest_longitude_sensor_1
    global latest_latitude_sensor_0, latest_latitude_sensor_1

    if senderStamp == 0:  # Assuming '0' refers to sensor opendlv-device-gps-ncom-0
        latest_longitude_sensor_0 = longitude
        latest_latitude_sensor_0 = latitude
    elif senderStamp == 1:  # Assuming '1' refers to sensor opendlv-device-gps-ncom-1
        latest_longitude_sensor_1 = longitude
        latest_latitude_sensor_1 = latitude
    else:
        print(f"Unknown sensor with senderStamp={senderStamp}")


# Callback function to handle received Steering messages
def onSteering(msg, senderStamp, timeStamps):
    # Extract steering attributes
    road_wheel_angle = msg.roadWheelAngle

    global latest_steering_angle
    latest_steering_angle = road_wheel_angle  # You can choose which angle to store



# Callback function to handle received AngleReading messages
def onAngleReading(msg, senderStamp, timeStamps):
    # Extract angle
    angle = msg.angle


    global latest_angle_reading
    latest_angle_reading = angle
    print("-" * 50)


def main():
    try:
        print("Listener script is starting...")

        # Specify the CID (Communication ID) used by your OD4 session.
        cid = 100  # Replace with your actual CID if different

        # Create an OD4Session instance.
        session = OD4Session(cid)

        # Message IDs
        messageIDGeolocation = 1116  # opendlv.logic.sensation.Geolocation
        messageIDSteering = 199  # opendlv.proxy.rhino.Steering
        messageIDAngleReading = 1038  # opendlv.proxy.AngleReading

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
            time.sleep(1)
            # Print the latest data from both sensors
            if latest_longitude_sensor_0 is not None and latest_latitude_sensor_0 is not None:
                print(f"Sensor 0 - Latest Longitude: {latest_longitude_sensor_0}, Latitude: {latest_latitude_sensor_0}")
            else:
                print("No data received yet from Sensor 0.")

            if latest_longitude_sensor_1 is not None and latest_latitude_sensor_1 is not None:
                print(f"Sensor 1 - Latest Longitude: {latest_longitude_sensor_1}, Latitude: {latest_latitude_sensor_1}")
            else:
                print("No data received yet from Sensor 1.")

            # Print the latest Steering angle
            if latest_steering_angle is not None:
                print(f"Latest Steering Angle: {latest_steering_angle}")
            else:
                print("No steering data received yet.")

            # Print the latest AngleReading
            if latest_angle_reading is not None:
                print(f"Latest Angle Reading: {latest_angle_reading}")
            else:
                print("No angle reading data received yet.")

            print("-" * 50)

            while True:
                time.sleep(0.05)  # Match the rate in your Unity coroutine

                data = {
                    'longitude_sensor_0': latest_longitude_sensor_0,
                    'latitude_sensor_0': latest_latitude_sensor_0,
                    'longitude_sensor_1': latest_longitude_sensor_1,
                    'latitude_sensor_1': latest_latitude_sensor_1,
                    'steering_angle': latest_steering_angle,
                    'angle_reading': latest_angle_reading
                }

                # Serialize data to JSON
                json_data = json.dumps(data)

                # Send data over UDP
                sock.sendto(json_data.encode('utf-8'), (UNITY_IP, UNITY_PORT))

                print(f"Sent data to Unity: {json_data}")

    except Exception as e:
        print(f"An error occurred in listener: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Listener stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()

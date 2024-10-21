#!/usr/bin/env python3
import sys
import time
from OD4Session import OD4Session
import opendlv_standard_message_set_v0_9_10_pb2

def main():
    # Specify the CID (Communication ID) used by your OD4 session.
    cid = 100  # Must match the CID in listener.py

    # Create an OD4Session instance.
    session = OD4Session(cid)

    # Connect to the network session.
    session.connect()
    print("Sender connected to OD4 session.")

    # Message IDs for opendlv.logic.sensation.Geolocation, opendlv.proxy.rhino.Steering, and opendlv.proxy.AngleReading
    messageIDGeolocation = 1116
    messageIDSteering = 199
    messageIDAngleReading = 1038

    # Initialize starting values for sensors and devices
    longitude_sensor_0 = 0.0
    longitude_sensor_1 = 10.0
    road_wheel_angle = 0.0
    angle_value = 5.0

    try:
        while True:
            # --- Send Geolocation message for Sensor 0 (opendlv-device-gps-ncom-0) ---
            geolocation_msg_0 = opendlv_standard_message_set_v0_9_10_pb2.opendlv_logic_sensation_Geolocation()
            geolocation_msg_0.longitude = longitude_sensor_0
            geolocation_msg_0.latitude = 0.0  # Optional: Set latitude if needed

            # Serialize the message
            serialized_msg_0 = geolocation_msg_0.SerializeToString()

            # Send the message with senderStamp = 0 (for sensor 0)
            session.send(messageIDGeolocation, serialized_msg_0, senderStamp=0)
            print(f"Sent Geolocation message from Sensor 0 with longitude: {longitude_sensor_0}")

            # Increment longitude for demonstration purposes (Sensor 0)
            longitude_sensor_0 += 0.1

            # --- Send Geolocation message for Sensor 1 (opendlv-device-gps-ncom-1) ---
            geolocation_msg_1 = opendlv_standard_message_set_v0_9_10_pb2.opendlv_logic_sensation_Geolocation()
            geolocation_msg_1.longitude = longitude_sensor_1
            geolocation_msg_1.latitude = 0.0  # Optional: Set latitude if needed

            # Serialize the message
            serialized_msg_1 = geolocation_msg_1.SerializeToString()

            # Send the message with senderStamp = 1 (for sensor 1)
            session.send(messageIDGeolocation, serialized_msg_1, senderStamp=1)
            print(f"Sent Geolocation message from Sensor 1 with longitude: {longitude_sensor_1}")

            # Increment longitude for demonstration purposes (Sensor 1)
            longitude_sensor_1 += 0.1

            # --- Send Steering message ---
            steering_msg = opendlv_standard_message_set_v0_9_10_pb2.opendlv_proxy_rhino_Steering()
            steering_msg.roadWheelAngle = road_wheel_angle
            steering_msg.steeringWheelAngle = road_wheel_angle  # You can adjust or simulate different values

            # Serialize the message
            serialized_steering_msg = steering_msg.SerializeToString()

            # Send the steering message
            session.send(messageIDSteering, serialized_steering_msg)
            print(f"Sent Steering message with road wheel angle: {road_wheel_angle}")

            # Increment steering angle for demonstration purposes
            road_wheel_angle += 0.05

            # --- Send AngleReading message ---
            angle_reading_msg = opendlv_standard_message_set_v0_9_10_pb2.opendlv_proxy_AngleReading()
            angle_reading_msg.angle = angle_value

            # Serialize the message
            serialized_angle_msg = angle_reading_msg.SerializeToString()

            # Send the angle reading message
            session.send(messageIDAngleReading, serialized_angle_msg)
            print(f"Sent AngleReading message with angle: {angle_value}")

            # Increment angle value for demonstration purposes
            angle_value += 0.1

            # Wait for 1 second before sending the next set of messages
            time.sleep(1)

    except KeyboardInterrupt:
        print("Sender stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred in sender: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

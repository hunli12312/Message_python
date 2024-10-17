#!/usr/bin/env python3
import sys
import time
from OD4Session import OD4Session
import opendlv_standard_message_set_v0_9_10_pb2

def main():
    # Specify the CID (Communication ID) used by your OD4 session.
    cid = 111  # Must match the CID in listener.py

    # Create an OD4Session instance.
    session = OD4Session(cid)

    # Connect to the network session.
    session.connect()
    print("Sender connected to OD4 session.")

    # Message ID for opendlv.logic.sensation.Geolocation
    # Replace '1030' with the actual message ID from your .odvd file if different.
    messageIDGeolocation = 1116

    # Initialize starting longitude value
    current_longitude = 0.0

    try:
        while True:
            # Create a Geolocation message
            geolocation_msg = opendlv_standard_message_set_v0_9_10_pb2.opendlv_logic_sensation_Geolocation()
            geolocation_msg.longitude = current_longitude
            geolocation_msg.latitude = 0.0  # Optional: Set latitude if needed

            # Serialize the message
            serialized_msg = geolocation_msg.SerializeToString()

            # Send the message
            session.send(messageIDGeolocation, serialized_msg)
            print(f"Sent Geolocation message with longitude: {current_longitude}")

            # Increment longitude for demonstration purposes
            current_longitude += 0.1

            # Wait for 1 second before sending the next message
            time.sleep(1)

    except KeyboardInterrupt:
        print("Sender stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred in sender: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

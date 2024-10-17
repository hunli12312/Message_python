#!/usr/bin/env python3

# Import necessary modules
import sys
import time
from OD4Session import OD4Session
import opendlv_standard_message_set_v0_9_10_pb2

# Variable to store the latest longitude value
latest_longitude = None

# Callback function to handle received Geolocation messages
def onGeolocation(msg, senderStamp, timeStamps):
    sent, received, sampleTimeStamp = timeStamps
    print(f"Received Geolocation; senderStamp= {senderStamp}")
    print(f"Sent at: {sent}")
    print(f"Received at: {received}")
    print(f"Sampled at: {sampleTimeStamp}")
    print(f"Message content: {msg}")
    
    # Extract longitude
    longitude = msg.longitude
    print(f"Longitude: {longitude}")
    
    global latest_longitude
    latest_longitude = longitude
    print("-" * 50)

def main():
    try:
        print("Listener script is starting...")
        
        # Specify the CID (Communication ID) used by your OD4 session.
        cid = 111  # Replace with your actual CID if different

        # Create an OD4Session instance.
        session = OD4Session(cid)

        # Message ID for opendlv.logic.sensation.Geolocation
        # Replace '1030' with the actual message ID from your .odvd file if different.
        messageIDGeolocation = 1116

        # Register callback for the Geolocation message
        session.registerMessageCallback(
            messageIDGeolocation,
            onGeolocation,
            opendlv_standard_message_set_v0_9_10_pb2.opendlv_logic_sensation_Geolocation
        )

        # Connect to the network session.
        session.connect()
        print("Listener connected to OD4 session.")

        print("Listener started. Waiting for messages...")

        while True:
            # Sleep to reduce CPU usage
            time.sleep(1)
            # Optionally, print the latest longitude
            if latest_longitude is not None:
                print(f"Latest Longitude: {latest_longitude}")
            else:
                print("No longitude data received yet.")
            print("-" * 50)
    except Exception as e:
        print(f"An error occurred in listener: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Listener stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()

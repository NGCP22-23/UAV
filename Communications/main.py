from Client import Client
import time
import sys

# append the path of the
# parent directory
sys.path.append("..")

from Autonomous.Plane import Plane
 
# Connect to the pixhawk
plane = Plane('/dev/ttyACM0')

# Create client
client = Client()


def send_telemetry_data():
    endpoint = 'http://10.110.180.122:5000/telemetry'
    client.send_post(endpoint, plane.getTelemetryData())

# while(True):
#     send_telemetry_data()
#     time.sleep(3)


# monitor mission
nextwaypoint = plane.vehicle.commands.next
while nextwaypoint < len(plane.vehicle.commands):
    if plane.vehicle.commands.next > nextwaypoint:
        display_seq = plane.vehicle.commands.next
        #if takeoff command is added, the waypoints will be 1 off
        print("Moving to waypoint %s" % display_seq)
        nextwaypoint = display_seq
    send_telemetry_data()
    time.sleep(3)



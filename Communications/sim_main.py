from Client import Client
import time
import sys

# append the path of the
# parent directory
sys.path.append("..")

from Autonomous.Plane import Plane

# Connect to Simulation
plane = Plane('tcp:127.0.0.1:5762')

# Create client
client = Client()


def send_telemetry_data():
    endpoint =  'http://192.168.50.37:5000/telemetry'
    client.send_post(endpoint, plane.getTelemetryData())

# arm and takeoff(for sim)
plane.arm_and_takeoff()

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



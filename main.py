import dronekit
from Autonomous import Plane 
from Communications import Client
import time

# Connect to the pixhawk
plane = Plane.Plane('/dev/ttyACM0')

# Create client
client = Client.Client()


def send_telemetry_data():
    endpoint = 'http://127.0.0.1:5000/telemetry'
    # store data in dictionary
    #data = {
        #data gets updated via listners in the Plane class upon update
        #consider sending messages at a consistent interval (1 sec?)
    #}
    #send data and enpoint to client\
    client.send_post(endpoint, plane.getTelemetryData())


# monitor mission
nextwaypoint = plane.vehicle.commands.next
while nextwaypoint < len(plane.vehicle.commands):
    if plane.vehicle.commands.next > nextwaypoint:
        display_seq = plane.vehicle.commands.next
        #if takeoff command is added, the waypoints will be 1 off
        print("Moving to waypoint %s" % display_seq)
        nextwaypoint = display_seq
    send_telemetry_data()
    time.sleep(1)

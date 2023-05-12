#import collections
#import collections.abc
#collections.MutableMapping = collections.abc.MutableMapping
#import dronekit
import Plane
import time
from create_mission import create_mission
import Client

# Connect to the pixhawk
#plane = Plane.Plane('/dev/ttyACM0')

# Connect to sim
plane = Plane.Plane('tcp:127.0.0.1:5762')

#plane.arm()
'''print("setup")
plane.operate_payload_door(False)
plane.payload_release_pins(False)
input("[ENTER]: Open Door")
plane.operate_payload_door(True)
input("[ENTER]: Release Pins")
plane.payload_release_pins(True)
input("[ENTER]: Close Door")
plane.operate_payload_door(False)'''
# tgt_lat, tgt_long, approach_heading, drop_offset, altitudeAGL, approach_distance

# plane = Plane.Plane('tcp:127.0.0.1:5762')

client = Client.Client()

test_servo_id = 8
# plane.arm()
# while True:
#     print("moving motor")
#     plane.rotate_target_servo(test_servo_id, pwm_value_int=1100)
#     time.sleep(1)
#     plane.rotate_target_servo(test_servo_id, pwm_value_int=1900)
#     time.sleep(1)


#plane.payload_drop_handler(34.04331760, -117.81297297, 40, 50, 50, 300)
#I seperated the mission creation from the demo file and stored it in create_mission.py
create_mission(plane)

#arm the plane
#plane.arm()
#The mission is downloaded and the plane is ready to fly
 
#through command proxy/controller set to manual
#through command proxy/controller set to auto

endpoint = 'http://127.0.0.1:5000/telemetry'

# monitor mission execution
nextwaypoint = plane.vehicle.commands.next
while nextwaypoint < len(plane.vehicle.commands):
    if plane.vehicle.commands.next > nextwaypoint:
        display_seq = plane.vehicle.commands.next
        #if takeoff command is added, the waypoints will be 1 off
        print("Moving to waypoint %s" % display_seq)
        nextwaypoint = display_seq
    #print("nothing to report")
    #print(plane.getTelemetryData()
    client.send_post(endpoint, plane.getTelemetryData())
    
    time.sleep(1)


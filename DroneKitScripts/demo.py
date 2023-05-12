import collections
import collections.abc
collections.MutableMapping = collections.abc.MutableMapping
import dronekit
import Plane
import time
#from . import create_mission

# Connect to the pixhawk
#plane = Plane.Plane('/dev/ttyACM0')

# Connect to sim
plane = Plane.Plane('tcp:127.0.0.1:5762')

plane.arm()
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
plane.payload_drop_handler(34.04331760, -117.81297297, 40, 50, 50, 300)

#arm the plane
#plane.arm()
#The mission is downloaded and the plane is ready to fly
 
#through command proxy/controller set to manual
#through command proxy/controller set to auto

# monitor mission execution
'''nextwaypoint = plane.vehicle.commands.next
while nextwaypoint < len(plane.vehicle.commands):
    if plane.vehicle.commands.next > nextwaypoint:
        display_seq = plane.vehicle.commands.next+1
        print("Moving to waypoint %s" % display_seq)
        nextwaypoint = plane.vehicle.commands.next
    time.sleep(1)'''


#import collections
#import collections.abc
#collections.MutableMapping = collections.abc.MutableMapping
import dronekit
import Plane
import time
from . import create_mission

# Connect to the pixhawk
plane = Plane.Plane('/dev/ttyACM0')

# Connect to sim
#plane = Plane.Plane('tcp:127.0.0.1:5762')

test_servo_id = 8
# plane.arm()
# while True:
#     print("moving motor")
#     plane.rotate_target_servo(test_servo_id, pwm_value_int=1100)
#     time.sleep(1)
#     plane.rotate_target_servo(test_servo_id, pwm_value_int=1900)
#     time.sleep(1)



#I seperated the mission creation from the demo file and stored it in create_mission.py
create_mission(plane)

#arm the plane
plane.arm()
#The mission is downloaded and the plane is ready to fly
 
#through command proxy/controller set to manual
#through command proxy/controller set to auto

# monitor mission execution
nextwaypoint = plane.vehicle.commands.next
while nextwaypoint < len(plane.vehicle.commands):
    if plane.vehicle.commands.next > nextwaypoint:
        display_seq = plane.vehicle.commands.next+1
        print("Moving to waypoint %s" % display_seq)
        nextwaypoint = plane.vehicle.commands.next
    time.sleep(1)


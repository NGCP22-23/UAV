#import collections
#import collections.abc
#collections.MutableMapping = collections.abc.MutableMapping
import dronekit
import Plane
import time

# Connect to the pixhawk
# plane = Plane.Plane('/dev/ttyACM0')

# Connect to sim
plane = Plane.Plane('tcp:127.0.0.1:5762')

#clear any stored mission
plane.clear_mission

#mission list will store all desired commands
missionList = []

#(for sim) add takeoff command
missionList.append(plane.create_takeoff_command(100, 40))

#add desired waypoints to mission list
altitudeAGL = 60.96 #meters = 200ft
missionList.append(plane.create_waypoint_command(34.042779, -117.815004, altitudeAGL))
missionList.append(plane.create_waypoint_command(34.04438421571916, -117.8134407649254, altitudeAGL))
missionList.append(plane.create_waypoint_command(34.043226, -117.8117594, altitudeAGL))
missionList.append(plane.create_waypoint_command(34.041962, -117.813311, altitudeAGL))

#create mission with mission list
plane.create_mission(missionList)

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


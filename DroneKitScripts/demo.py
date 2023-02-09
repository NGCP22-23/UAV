# 1. Connect Jetson and Pixhawk
#    - run connection test script to ensure connection
# 2. Change to manual mode via controller
# 3. Takoff through manual controls
# 4. Change to auto mode via controller
#   -if the plane is in the air, then changing mode to auto is all that is required to start the mission
# 5. The preloaded mission should be ran 
# 6. Once the mission is complete, manual mode is set by controller and manual landing is done

# possible things to add: 
#   - distance to waypoint(function already in https://dronekit-python.readthedocs.io/en/latest/guide/auto_mode.html#auto-mode-vehicle-control)
#   - change the file so that when vehicle mode is set to auto it runs preloaded mission
#   - add guided, rtl at end of mission
#   
# documentation on plane commands: https://ardupilot.org/plane/docs/common-mavlink-mission-command-messages-mav_cmd.html#commands-supported-by-plane 
# documentation on basic mission: https://dronekit-python.readthedocs.io/en/latest/examples/mission_basic.html


import dronekit
import Plane

# Connect to the pixhawk or sim
# plane = Plane(conection_string = '/dev/ttyACM0')
plane = Plane.Plane('tcp:127.0.0.1:5762')
#clear any stored mission
plane.clear_mission

#mission list will store all desired commands
missionList = []

#(for sim) add takeoff command
missionList.append(plane.create_takeoff_command(100, 40))
#add desired waypoints to mission list
missionList.append(plane.create_waypoint_command(34.04257370, -117.81366938))
missionList.append(plane.create_waypoint_command(34.04334701, -117.81425840))
missionList.append(plane.create_waypoint_command(34.04388579, -117.81343224))

#create mission with mission list
plane.create_mission(missionList)

#(for sim)run arm_and_takeoff
plane.arm_and_takeoff()



#34.04257370 -117.81366938 
#34.04334701 -117.81425840
#34.04388579 -117.81343224
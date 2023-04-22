from Autonomous import Plane 

# Connect to the pixhawk
plane = Plane.Plane('/dev/ttyACM0')


#recieves a plane vehicle object and sets a a mission
def create_mission(plane):
    #clear any stored mission
    plane.clear_mission

    #mission list will store all desired commands
    missionList = []

    #(for sim) add takeoff command
    # missionList.append(plane.create_takeoff_command(100, 40))

    #add desired waypoints to mission list
    altitudeAGL = 60.96 #meters = 200ft
    missionList.append(plane.create_waypoint_command(34.041464376161, -117.81479888146936, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.04276497765443, -117.8157547651131, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.042809752107, -117.81374196205198, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.04400745993929, -117.81457950426534, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.043873138407704, -117.81299898105624, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.04489173804476, -117.8134312609083, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.043335850153895, -117.81333669969067, altitudeAGL))


    #create mission with mission list
    plane.create_mission(missionList)


create_mission(plane)
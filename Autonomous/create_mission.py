
#recieves a plane vehicle object and sets a a mission
def create_mission(plane):
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
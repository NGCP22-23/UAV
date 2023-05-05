import Plane 

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

    # #(for sim) add takeoff command
    # missionList.append(plane.create_takeoff_command(100, 40))   

    # 1500 ft
    # missionList.append(plane.create_waypoint_command(34.04019690319695, -117.81620860314962, altitudeAGL))


    # 1000ft
    # missionList.append(plane.create_waypoint_command(34.04116297537259, -117.81520557977723, altitudeAGL))
    # missionList.append(plane.create_waypoint_command(34.04329854577586, -117.81539298653017, altitudeAGL))
    # missionList.append(plane.create_waypoint_command(34.041715365774586, -117.81468460112269, altitudeAGL))
    # missionList.append(plane.create_waypoint_command(34.042615893674245, -117.81587781029921, altitudeAGL))

    # 500ft
    missionList.append(plane.create_waypoint_command(34.04238195873398, -117.81411424697538, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.04329854577586, -117.81539298653017, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.04274024693057, -117.81366584755779, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.04364554486393, -117.81518474806516, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.04313769599379, -117.81335940271858, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.04406368166445, -117.81455317466148, altitudeAGL))
    missionList.append(plane.create_waypoint_command(34.043343890954105, -117.81308056937189, altitudeAGL))


    #create mission with mission list
    plane.create_mission(missionList)


create_mission(plane)
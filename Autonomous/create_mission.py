import Plane 

# Connect to the pixhawk
plane = Plane.Plane('/dev/ttyACM0')


#recieves a plane vehicle object and sets a a mission
def create_mission(coords, alt):
    #clear any stored mission
    plane.clear_mission

    #mission list will store all desired commands
    missionList = []

    #(for sim) add takeoff command
    # missionList.append(plane.create_takeoff_command(100, 40))

    #add desired waypoints to mission list
    altitudeAGL = alt #meters = 200ft

    for coord in coords:
        missionList.append(plane.create_waypoint_command(coord[0], coord[1], alt))

    
    #create mission with mission list
    plane.create_mission(missionList)



waypoints_500ft = [[34.04238195873398, -117.81411424697538], [34.04329854577586, -117.81539298653017],[34.04274024693057, -117.81366584755779],[34.04364554486393, -117.81518474806516], [34.04313769599379, -117.81335940271858], [34.04406368166445, -117.81455317466148], [34.043343890954105, -117.81308056937189] ]
waypoints_1000ft = [[34.04116297537259, -117.81520557977723], [34.04329854577586, -117.8153929865301], [34.041715365774586, -117.81468460112269], [34.042615893674245, -117.81587781029921]]
waypoints_1500ft = [[34.04019690319695, -117.81620860314962],[34.040970917448796, -117.81703946642989], [34.0411072823772, -117.81596242089414]]
waypoints_fire = [[34.042070420295225, -117.81324461818397], [34.042960474069226, -117.81468029364673], [34.04219633090855, -117.81302979083371], [34.04310809184083, -117.81460169827471], [34.04240039254003, -117.81279924440904],[34.04342069333253, -117.81368999195894], [34.042838906299664, -117.81248486292085] ]

mission1 = waypoints_500ft
mission2 = waypoints_1000ft + waypoints_500ft
mission3 = waypoints_1500ft + mission2
altitude = 60.96 #200 ft

#create_mission(mission2, altitude)
create_mission(waypoints_fire, 30.48)

from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, Battery, LocationGlobal, Attitude
from pymavlink import mavutil


import time
import math


import rclpy 
from rclpy.node import Node
from std_msgs.msg import String


PAYLOAD_PIN = 7
PAYLOAD_DOOR = 8

PIN_SERVO_IN_PWM = 2200.0
PIN_SERVO_OUT_PWM = 800.0
DOOR_SERVO_PWM_OPEN = 1650.0
DOOR_SERVO_PWM_CLOSED = 850.0



class Plane(Node):

    def __init__(self, connection_string=None, vehicle=None):
        # ros node initialization
        super().__init__('plane_node')

        # ros publisher topics
        self.telem_publisher = self.create_publisher(String, 'telem', 10)

        # set rate of publishing 
        self.timer_period = 1   #1 second(1Hz)
        self.mode_timer = self.create_timer(self.timer_period, self.telem_publisher_callback)

        # ros subscriber topics
        self.mission_subscriber= self.create_subscription(String, 'mission', self.mission_subscriber_callback, 10)
        self.hiker_coords_subscriber =self.create_subscription(String, 'hikerCoords', self.payload_callback, 10)

        """ Initialize the object
        Use either the provided vehicle object or the connections tring to connect to the autopilot

        Input:
            connection_string       - the mavproxy style connection string, like tcp:127.0.0.1:5760
                                      default is None
            vehicle                 - dronekit vehicle object, coming from another instance (default is None)
        """

        #---- Connecting with the vehicle, using either the provided vehicle or the connection string

        if not vehicle is None:
            self.vehicle    = vehicle
            print("Using the provided vehicle")

        elif not connection_string is None:
            print("Connecting with vehicle...")
            self._connect(connection_string)
            print("Successfully connected with vehicle")

        else:
            raise("ERROR: a valid dronekit vehicle or a connection string must be supplied")
            return

            
        self.wind_dir_to_deg    = 0.0       #- [deg]    wind direction (where it is going)
        self.wind_dir_from_deg  = 0.0       #- [deg]    wind coming from direction
        self.wind_speed         = 0.0       #- [m/s]    wind speed

        self.climb_rate         = 0.0       #- [m/s]    climb rate
        self.throttle           = 0.0       #- [ ]      throttle (0-100)

        self._setup_listeners()

        self.airspeed           = 0.0       #- [m/s]    airspeed
        self.groundspeed        = 0.0       #- [m/s]    ground speed

        self.pos_lat            = 0.0       #- [deg]    latitude
        self.pos_lon            = 0.0       #- [deg]    longitude
        self.pos_alt_rel        = 0.0       #- [m]      altitude relative to takeoff
        self.pos_alt_abs        = 0.0       #- [m]      above mean sea level

        
        self.att_roll_deg       = 0.0       #- [deg]    roll
        self.att_pitch_deg      = 0.0       #- [deg]    pitch
        self.att_heading_deg    = 0.0       #- [deg]    magnetic heading

        self.ap_mode            = ''        #- []       Autopilot flight mode
        self.mission            = self.vehicle.commands         #-- mission items
        self.location_home      = LocationGlobalRelative(0,0,0) #- LocationRelative type home
        self.location_current   = LocationGlobalRelative(0,0,0) #- LocationRelative type current position

        self.flight_plan        = ''      # saved to compare to new one which comes as a str from topic
        self.next_waypoint   = self.vehicle.commands.next

        # variables for max confidence value
        self.max_confidence = 0 
        self.hiker_lat = 0
        self.hiker_lon = 0

    def _connect(self, connection_string):      #-- (private) Connect to Vehicle

        """ (private) connect with the autopilot
        Input:
            connection_string   - connection string (mavproxy style)
        """

        self.vehicle = connect(connection_string, wait_ready= False, baud = 57600)
        self._setup_listeners()

    def _setup_listeners(self):                 #-- (private) Set up listeners

        #----------------------------
        #--- CALLBACKS
        #---------------------------
        #When the vehicle receives a message with the above string, it updates the plane variables
        #need to look more into what messages there are and what values we need to track

        if True:    
            #---- DEFINE CALLBACKS HERE!!!
            @self.vehicle.on_message('ATTITUDE')   
            def listener(vehicle, name, message):          #--- Attitude
                self.att_roll_deg   = math.degrees(message.roll)
                self.att_pitch_deg  = math.degrees(message.pitch)
                self.att_heading_deg = math.degrees(message.yaw)%360
                
            @self.vehicle.on_message('GLOBAL_POSITION_INT')       
            def listener(vehicle, name, message):          #--- Position / Velocity                                                                                                             
                self.pos_lat        = message.lat*1e-7
                self.pos_lon        = message.lon*1e-7
                self.pos_alt_rel    = message.relative_alt*1e-3
                self.pos_alt_abs    = message.alt*1e-3
                self.location_current = LocationGlobalRelative(self.pos_lat, self.pos_lon, self.pos_alt_rel)
         

            @self.vehicle.on_message('VFR_HUD')
            def listener(vehicle, name, message):          #--- HUD
                self.airspeed       = message.airspeed
                self.groundspeed    = message.groundspeed
                self.throttle       = message.throttle
                self.climb_rate     = message.climb 

                
            @self.vehicle.on_message('WIND')
            def listener(vehicle, name, message):          #--- WIND
                self.wind_speed         = message.speed
                self.wind_dir_from_deg  = message.direction % 360
                self.wind_dir_to_deg    = (self.wind_dir_from_deg + 180) % 360


        return (self.vehicle)

        print(">> Connection Established")

    def is_armed(self):                         #-- Check whether uav is armed
        """ Checks whether the UAV is armed
        """
        return(self.vehicle.armed)

        
    def arm(self):                              #-- arm the UAV
        """ Arm the UAV
        """
        self.vehicle.armed = True

    def disarm(self):                           #-- disarm UAV
        """ Disarm the UAV
        """
        self.vehicle.armed = False


    def set_airspeed(self, speed):              #--- Set target airspeed, default is 15m/s
        """ Set uav airspeed m/s
        """
        self.vehicle.airspeed = speed

    def set_ap_mode(self, mode):                #--- Set Autopilot mode
        """ Set Autopilot mode
        """
        time_0 = time.time()

        try:
            tgt_mode    = VehicleMode(mode)
        except:
            return(False)

        while (self.get_ap_mode() != tgt_mode):
            self.vehicle.mode  = tgt_mode
            time.sleep(0.2)
            if time.time() < time_0 + 5:
                return (False)

        return (True)

        
    def get_ap_mode(self):                      #--- Get the autopilot mode
        """ Get the autopilot mode
        """
        self._ap_mode  = self.vehicle.mode
        return(self.vehicle.mode)


    # ros publisher callback for mode
    def telem_publisher_callback(self):
        # build the message
        msg = String()
        telem = (
                str(self.pos_alt_abs), 
                str(self.airspeed), 
                str(self.att_pitch_deg), 
                str(self.att_roll_deg), 
                str(self.att_heading_deg),
                str(self.pos_lat), 
                str(self.pos_lon), 
                str(self.get_ap_mode()), 
                str(self.next_waypoint),
            )
        msg.data = '\n'.join(telem)

        # publish the data 
        self.telem_publisher.publish(msg)

        # print to console
        # self.get_logger().info('Publishing: "%s"' % msg.data)


    # ros subscriber callback function for changing mission from mission topic
    def mission_subscriber_callback(self, msg):
        self.flight_plan = msg.data

        mission_list = []
        alt = 60.96

        coordinates = self.flight_plan.split('\n')
        
        i = 0
        for i in range(len(coordinates)):
            if i == len(coordinates)-1:
                break

            x = coordinates[i].split(', ')
            print(x)
            mission_list.append(self.create_waypoint_command(float(x[0]), float(x[1]), alt))
        
        self.create_mission(mission_list)
        # self.get_logger().info('I heard: "%s"' % msg.data)

    def payload_callback(self, msg):
        print('\n\n\n----------------------Commencing Payload Mission-----------------------\n')

        # split into list
        hiker_coords = msg.data.split('\n')

        approach_heading = self.att_heading_deg
        # make sure its within 0-360
        if self.att_heading_deg + 90 > 360:
            approach_heading = self.att_heading - 360

        
        self.payload_drop_handler(hiker_coords[0], hiker_coords[1], approach_heading)
            
    def clear_mission(self):                    #--- Clear the onboard mission
        """ Clear the current mission.
        """
        cmds = self.vehicle.commands
        self.vehicle.commands.clear()
        self.vehicle.flush()


        # After clearing the mission you MUST re-download the mission from the vehicle
        # before vehicle.commands can be used again
        # (see https://github.com/dronekit/dronekit-python/issues/230)

        self.mission = self.vehicle.commands
        self.mission.download()
        self.mission.wait_ready()



    def download_mission(self):                 #--- download the mission

        """ Download the current mission from the vehicle.
        """

        self.vehicle.commands.download()
        self.vehicle.commands.wait_ready() # wait until download is complete.  
        self.mission = self.vehicle.commands

    

    def create_mission(self, commandsList):
        print('\n\nClearing current mission')
        self.clear_mission()
        cmds = self.vehicle.commands

        for cmd in commandsList:
            cmds.add(cmd)

        print('\nUploading new commands to vehicle')
        cmds.upload()
        print('Upload Complete\n\n')


    def create_waypoint_command(self, lat, lon, alt):
        return Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, lat, lon, alt)


    def create_takeoff_command(self, takeoff_altitude = 100, takeoff_pitch = 40):
        return Command( 0, 0, 0, 3, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, takeoff_pitch,  0, 0, 0, 0,  0, takeoff_altitude)


    def mission_add_takeoff(self, takeoff_altitude=50, takeoff_pitch=15, heading=None):

        """ Adds a takeoff item to the UAV mission, if it's not defined yet
        
        Input:

            takeoff_altitude    - [m]   altitude at which the takeoff is considered over
            takeoff_pitch       - [deg] pitch angle during takeoff
            heading             - [deg] heading angle during takeoff (default is the current)

        """

        if heading is None: heading = self.att_heading_deg

        self.download_mission()

        #-- save the mission: copy in the memory
        tmp_mission = list(self.mission)

       # print tmp_mission.count
        is_mission  = False

        if len(tmp_mission) >= 1:
            is_mission = True
            print("Current mission:")

            #for item in tmp_mission:
               # print item

            #-- If takeoff already in the mission, do not do anything
            

        if is_mission and tmp_mission[0].command == mavutil.mavlink.MAV_CMD_NAV_TAKEOFF:
            print ("Takeoff already in the mission")

        else:
            print("Takeoff not in the mission: adding")

            self.clear_mission()
            takeoff_item = Command( 0, 0, 0, 3, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, takeoff_pitch,  0, 0, 0, 0,  0, takeoff_altitude)
            self.mission.add(takeoff_item)

            for item in tmp_mission:
                self.mission.add(item)
            self.vehicle.flush()

            print(">>>>>Done")

        

    def arm_and_takeoff(self, altitude=100, pitch_deg=40):

        """ Arms the UAV and takeoff
        Planes need a takeoff item in the mission and to be set into AUTO mode. The 
        heading is kept constant

        Input:

            altitude    - altitude at which the takeoff is concluded
            pitch_deg   - pitch angle during takeoff

        """



        self.mission_add_takeoff(takeoff_altitude=1.5*altitude, takeoff_pitch=pitch_deg)
        print ("Takeoff mission ready")

        

        while not self.vehicle.is_armable:
            print("Wait to be armable...")
            time.sleep(1.0)
        
        #-- Save home
        while self.pos_lat == 0.0:
            time.sleep(0.5)
            print ("Waiting for good GPS...")

        self.location_home   = LocationGlobalRelative(self.pos_lat,self.pos_lon,altitude)

        print("Home is saved as " + str(self.location_home))
        print ("Vehicle is Armable: try to arm")

        self.set_ap_mode("MANUAL")

        n_tries = 0

        while not self.vehicle.armed:

            print("Try to arm...")
            self.arm()
            n_tries += 1
            time.sleep(2.0) 

            if n_tries > 5:
                print("!!! CANNOT ARM")
                break

        #--- Set to auto and check the ALTITUDE

        if self.vehicle.armed: 
            print ("ARMED")
            self.set_ap_mode("AUTO")

            time.sleep(20.0)

            print("Going home")
            self.set_ap_mode("RTL")

        return True

    

    def rotate_target_servo(self, servo_id, pwm_value_int):

        #https://dronekit-python.readthedocs.io/en/latest/guide/copter/guided_mode.html

        #https://ardupilot.org/plane/docs/common-mavlink-mission-command-messages-mav_cmd.html#mav-cmd-do-set-servo

        #https://discuss.ardupilot.org/t/aux-servos-via-dronekit/18716

        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,   #target sys, target_component
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0, #confirmation
            servo_id,
            pwm_value_int,
            0, 0, 0, 0, 0
        )

        self.vehicle.send_mavlink(msg)


    def operate_payload_door(self, open = True):

        if open:
            pwm = 1600  #TODO: Check Correct PWM rotation
        else:
            pwm = 1400  ##TODO: Check Correct PWM rotation
        self.rotate_target_servo(PAYLOAD_DOOR, pwm)
        return True

    

    def payload_release_pins(self, release = True):
        if release:
            pwm_release = 1400  ##TODO: Check Correct PWM rotation!
        else:
            # Set pints back into place
            pwm_release = 1600  ##TODO: Check Correct PWM rotation

        self.rotate_target_servo(PAYLOAD_PIN_A, pwm_release)
        self.rotate_target_servo(PAYLOAD_PIN_A, pwm_release)



    def get_target_from_bearing(self, original_location, ang, dist, altitude=None):

        """ Create a TGT request packet located at a bearing and distance from the original point

        Inputs:
            ang     - [rad] Angle respect to North (clockwise) 
            dist    - [m]   Distance from the actual location
            altitude- [m]
        Returns:
            location - Dronekit compatible

        """


        if altitude is None: altitude = original_location.alt
        
        # print '---------------------- simulate_target_packet'
        dNorth  = dist*math.cos(ang)
        dEast   = dist*math.sin(ang)

        # print "Based on the actual heading of %.0f, the relative target's coordinates are %.1f m North, %.1f m East" % (math.degrees(ang), dNorth, dEast) 

        #-- Get the Lat and Lon
        tgt     = self._get_location_metres(original_location, dNorth, dEast)

        tgt.alt = altitude

        # print "Obtained the following target", tgt.lat, tgt.lon, tgt.alt

        return tgt      

    

    def _get_location_metres(self, original_location, dNorth, dEast, is_global=False):

        """
        Returns a Location object containing the latitude/longitude `dNorth` and `dEast` metres from the
        specified `original_location`. The returned Location has the same `alt and `is_relative` values
        as `original_location`.
        The function is useful when you want to move the vehicle around specifying locations relative to
        the current vehicle position.
        The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.

        For more information see:
        http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters

        """

        earth_radius=6378137.0 #Radius of "spherical" earth

        #Coordinate offsets in radians
        dLat = dNorth/earth_radius
        dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))



        #New position in decimal degrees
        newlat = original_location.lat + (dLat * 180/math.pi)
        newlon = original_location.lon + (dLon * 180/math.pi)

        

        if is_global:
            return LocationGlobal(newlat, newlon,original_location.alt)    
        else:

            return LocationGlobalRelative(newlat, newlon,original_location.alt)         

    def rotate_target_servo(self, servo_id, pwm_value_int):
            #https://dronekit-python.readthedocs.io/en/latest/guide/copter/guided_mode.html
            #https://ardupilot.org/plane/docs/common-mavlink-mission-command-messages-mav_cmd.html#mav-cmd-do-set-servo
            #https://discuss.ardupilot.org/t/aux-servos-via-dronekit/18716
            msg = self.vehicle.message_factory.command_long_encode(
                0, 0,   #target sys, target_component
                mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
                0, #confirmation
                servo_id,
                pwm_value_int,
                0, 0, 0, 0, 0
            )
            self.vehicle.send_mavlink(msg)
        

    def operate_payload_door(self, open = True):
        if open:
            pwm = DOOR_SERVO_PWM_OPEN 
        else:
            pwm = DOOR_SERVO_PWM_CLOSED
        self.rotate_target_servo(PAYLOAD_DOOR, pwm)
        return True
    
    def payload_release_pins(self, release = True):
        if release:
            pwm_release = PIN_SERVO_OUT_PWM
        else:
            # Set pints back into place
            pwm_release = PIN_SERVO_IN_PWM  
        self.rotate_target_servo(PAYLOAD_PIN, pwm_release)

    # tgt_lat, tgt_long, approach_heading(angle from ), drop_offset(distance to drop), altitudeAGL, approach_distance(waypoint distance from target)
    def payload_drop_handler(self, tgt_lat, tgt_long, approach_heading = 0, drop_offset = 50, altitudeAGL = 100, approach_distance = 150): #values in meters
        successful_drop = False
        earth_radius = 6378137.0 #meters
        lat_change = (approach_distance * math.cos(math.radians(approach_heading)))/earth_radius
        long_change = (approach_distance * math.sin(math.radians(approach_heading)))/(earth_radius*math.cos(math.pi*tgt_lat/180))   #radians offset
        waypoints = []
        approach = [tgt_lat - (lat_change * 180/math.pi), tgt_long - (long_change * 180/math.pi)]
        missed_approach = [tgt_lat + (0.5 * lat_change * 180/math.pi), tgt_long + (0.5 * long_change * 180/math.pi)]
        drop_lat_change = (drop_offset * math.cos(math.radians(approach_heading)))/earth_radius
        drop_long_change = (drop_offset * math.sin(math.radians(approach_heading)))/(earth_radius*math.cos(math.pi*tgt_lat/180))   #radians offset
        target_offset = [tgt_lat - (drop_lat_change * 180/math.pi), tgt_long - (drop_long_change * 180/math.pi)]

        waypoints.append(self.create_waypoint_command(approach[0], approach[1], altitudeAGL))
        waypoints.append(self.create_waypoint_command(target_offset[0], target_offset[1], altitudeAGL))
        waypoints.append(self.create_waypoint_command(missed_approach[0], missed_approach[1], altitudeAGL))
        while not successful_drop:
            door_open = False
            self.clear_mission
            self.create_mission(waypoints)
            self.set_ap_mode("AUTO")
            print("[DROP NAV]: Started Approach Sequence")
            #dist = self.distance_to_coord(self.pos_lat, self.pos_lon, approach)
            #self.arm()
        
            if self.reached_point_get_status(approach[0], approach[1]) is True:
                print("[DROP NAV]: Reached Approach Point")
                if self.reached_point_get_status(tgt_lat, tgt_long) is True:
                    print("[DROP NAV]: Reached Drop Point Successful!")
                    successful_drop = True
                else:
                    print("[DROP NAV]: Did not reach drop point")
            else :
                print("[DROP NAV]: Did not reach approach point")

        pass

    # Returns true if aircraft reaches point on first attempt and must be heading towards point. False otherwise
    #TODO: Make sure this function does not disrupt other functions due to its while loop
    def reached_point_get_status(self, lat, long):
        dx = self.delta_distance(lat, long)
        #print(dx)
        while dx >= 0:
            print("Waiting until dx < 0")
            time.sleep(0.5)
            dx = self.delta_distance(lat, long)
            pass
        while dx < -0:   #less than5 m/s
            print(dx)
            dx = self.delta_distance(lat, long)
            if self.distance_to_coord(lat, long) < 20:
                return True
        return False    #Aircraft Did not get near enough to point and distance started increasing
    
    # Returns delta time in meters / second
    def delta_distance(self, lat, long):
        distance1 = self.distance_to_coord(lat, long)
        time.sleep(1)
        distance2 = self.distance_to_coord(lat, long)

        delta_unscaled = distance2 - distance1
        return delta_unscaled * 1


    def distance_to_coord(self, lat, long):
        lat1 = self.pos_lat
        long1 = self.pos_lon
        earth_radius = 6378137.0 #meters
        #Haversine Time
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat)
        dphi = math.radians(lat - lat1)
        dlambda = math.radians(long - long1)

        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        meters = earth_radius * c
        return meters 


def main(args=None):

    # initialize rclpy library
    rclpy.init(args=args)


    # creat the node
    plane_publisher = Plane('tcp:127.0.0.1:5762')


    # spin the node so callbacks are called
    rclpy.spin(plane_publisher)


    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    plane_publisher.destroy_node()

    rclpy.shutdown()





if __name__ == '__main__':
    main()


    # def ground_course_2_location(self, angle_deg, altitude=None):

    #     """ Creates a target to aim to in order to follow the ground course

    #     Input:

    #         angle_deg   - target ground course

    #         altitude    - target altitude (default the current)

        

    #     """

    #     tgt = self.get_target_from_bearing(original_location=self.location_current, 

    #                                          ang=math.radians(angle_deg), 

    #                                          dist=5000,

    #                                          altitude=altitude)

    #     return(tgt)

        

    # def goto(self, location):

    #     """ Go to a location

        

    #     Input:

    #         location    - LocationGlobal or LocationGlobalRelative object

        

    #     """

    #     self.vehicle.simple_goto(location)

 

    # def set_ground_course(self, angle_deg, altitude=None):

    #     """ Set a ground course

        

    #     Input:

    #         angle_deg   - [deg] target heading

    #         altitude    - [m]   target altitude (default the current)

        

    #     """

        

    #     #-- command the angles directly

    #     self.goto(self.ground_course_2_location(angle_deg, altitude))

        

    # def get_rc_channel(self, rc_chan, dz=0, trim=1500):         #--- Read the RC values from the channel

    #     """

    #     Gets the RC channel values with a dead zone around trim

        

    #     Input:

    #         rc_channel  - input rc channel number

    #         dz          - dead zone, within which the output is set equal to trim

    #         trim        - value about which the dead zone is evaluated

            

    #     Returns:

    #         rc_value    - [us]

    #     """

    #     if (rc_chan > 16 or rc_chan < 1):

    #         return -1

        

    #     #- Find the index of the channel

    #     strInChan = '%1d' % rc_chan

    #     try:

        

    #         rcValue = int(self.vehicle.channels.get(strInChan))

            

    #         if dz > 0:

    #             if (math.fabs(rcValue - trim) < dz):

    #                 return trim

            

    #         return rcValue

    #     except:

            # return 0     

    

    # def set_rc_channel(self, rc_chan, value_us=0):      #--- Overrides a rc channel (call with no value to reset)

    #     """

    #     Overrides the RC input setting the provided value. Call with no value to reset

        

    #     Input:

    #         rc_chan     - rc channel number

    #         value_us    - pwm value 

    #     """

    #     strInChan = '%1d' % rc_chan

    #     self.vehicle.channels.overrides[strInChan] = int(value_us)

                

    # def clear_all_rc_override(self):               #--- clears all the rc channel override

    #     self.vehicle.channels.overrides = {}

    





      


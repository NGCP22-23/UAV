
# import Node class
import rclpy
from rclpy.node import Node 

# import string message type 
from std_msgs.msg import String
from std_msgs.msg import Int32

import math
import time 

class FireLocator(Node):
    def __init__(self):
         # initialize super class
        super().__init__('fire_locator_node')

        self.lat = 0
        self.lon = 0
        self.heading = 0
        self.alt = 0

        self.dx = 0
        self.dy = 0


        # Create a telem subscription
        self.telem_subscriber = self.create_subscription(String, 'telem', self.telem_subscriber_callback, 10)
        self.dx_subscriber = self.create_subscription(Int32, 'dx', self.dx_subscriber_callback, 10)
        self.dy_subscriber = self.create_subscription(Int32, 'dy', self.dy_subscriber_callback, 10)

        # mission publisher
        self.fire_coords_publisher = self.create_publisher(String, 'fire_coords', 10)

        # # set rate of publishing 
        # self.timer_period = 1  #1 second(1Hz)
        # self.mode_timer = self.create_timer(self.timer_period, self.mission_publisher_callback)

    def telem_subscriber_callback(self, msg):
        # split into list
        telem_list = msg.data.split('\n')

        self.alt = telem_list[0]
        self.lat = telem_list[5]
        self.lon = telem_list[6]
        self.heading = telem_list[4]

    def dx_subscriber_callback(self, msg):
        self.dx = msg.data

    def dy_subscriber_callback(self, msg):
        self.dy = msg.data 
        time.sleep(.2)
        angle = self.calculate_angle_with_respect_to_north(self.dx, self.dy)
        print(angle)
        distance = self.calculate_hypotenuse(self.dx, self.dy)
        print(distance)
        gsd = self.ground_sample_distance_calculator(self.alt, distance)
        print(gsd)
        target_coords = self.get_target_from_bearing(self.lat, self.lon, angle + self.heading, gsd)
        print(target_coords)
        
        msg = String()
        msg.data = target_coords
        self.fire_coords_publisher.publish(msg)



    def calculate_angle_with_respect_to_north(self, dx, dy):
        angle_rad = math.atan2(dx, dy)
        angle_deg = math.degrees(angle_rad)
        angle_from_north = (angle_deg + 360) % 360
        return angle_from_north
        
    
    def calculate_hypotenuse(self, dx, dy):
        return math.sqrt(dx**2 + dy**2)

    # Takes altidue(m) and sample(pixels) and generates a distance in meters of the sample 
    def ground_sample_distance_calculator(self, altitude, sample_pixel_length):
        sensor_width = 4.96   # "mm"
        focal_length = 3.67     # "mm"
        image_width = 1920      # "pixel"      "resolution: 1920x1080"

        cm_per_pixel = (sensor_width*altitude*100)/(focal_length*image_width)     # "cm/pixel"

        return (cm_per_pixel*sample_pixel_length)/100        #  "m"
    

    def get_target_from_bearing(self, lat, lon, ang, dist):

        """ Create a TGT request packet located at a bearing and distance from the original point

        Inputs:
            ang     - [rad] Angle respect to North (clockwise) 
            dist    - [m]   Distance from the actual location
            altitude- [m]
        Returns:
            location - Dronekit compatible
        """
        
        # print '---------------------- simulate_target_packet'
        dNorth  = dist*math.cos(ang)
        dEast   = dist*math.sin(ang)

        # print "Based on the actual heading of %.0f, the relative target's coordinates are %.1f m North, %.1f m East" % (math.degrees(ang), dNorth, dEast) 

        #-- Get the Lat and Lon
        return self._get_location_metres(lat, lon, dNorth, dEast)

        # print "Obtained the following target", tgt.lat, tgt.lon, tgt.alt

        



    def _get_location_metres(self, lat, lon, dNorth, dEast, is_global=False):

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
        dLon = dEast/(earth_radius*math.cos(math.pi*lat/180))



        #New position in decimal degrees
        newlat = lat + (dLat * 180/math.pi)
        newlon = lon + (dLon * 180/math.pi)

        return f"{newlat}, {newlon}"

        # if is_global:
        #     return LocationGlobal(newlat, newlon, self.alt)    
        # else:

        #     return LocationGlobalRelative(newlat, newlon,self.alt)         


def main(args=None):
    rclpy.init(args=args)

    comms = FireLocator()

    # spin runs the callback functions
    rclpy.spin(comms)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    FireLocator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

# import Node class
import rclpy
from rclpy.node import Node 

# import string message type 
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

class FireLocator(Node):
    def __init__(self) -> None:
         # initialize super class
        super().__init__('fire_locator_node')

        self.lat = 0
        self.lon = 0
        self.heading = 0

        # Create a telem subscription
        self.telem_subscriber = self.create_subscription(String, 'telem', self.telem_subscriber_callback, 10)
        self.fire_detection_subscriber = self.create_subscription(Int32MultiArray, 'thresholds', self.fire_algo_subscriber_callback, 10)

        # mission publisher
        self.mission_publisher = self.create_publisher(String, 'mission', 10)

        # set rate of publishing 
        self.timer_period = 2  #1 second(1Hz)
        self.mode_timer = self.create_timer(self.timer_period, self.mission_publisher_callback)

    def telem_subscriber_callback(self, msg):
        # split into list
        telem_list = msg.data.split('\n')

        self.alt = telem_list[0]
        self.lat = telem_list[5]
        self.lon = telem_list[6]
        self.heading = telem_list[4]

    def fire_algo_subscriber_callback(self, msg):
        distance = msg.data 
        gsd = self.ground_sample_distance_calculator(self.alt, self.distance)
        print(gsd)




    

    # Takes altidue(m) and sample(pixels) and generates a distance in meters of the sample 
    def ground_sample_distance_calculator(self, altitude, sample_pixel_length):
        sensor_width = 4.96   # "mm"
        focal_length = 3.67     # "mm"
        image_width = 1920      # "pixel"      "resolution: 1920x1080"

        cm_per_pixel = (sensor_width*altitude*100)/(focal_length*image_width)     # "cm/pixel"

        # footprint_width = (cm_per_pixel*image_width)/100         #   "m"

        return (cm_per_pixel*sample_pixel_length)/100        #  "m"

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
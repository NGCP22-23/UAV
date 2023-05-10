from Client import Client
import time
import sys

# import Node class
import rclpy
from rclpy.node import Node 

# import string message type 
from std_msgs.msg import String

# append the path of the
# parent directory
sys.path.append("..")

from Autonomous.Plane import Plane
 
# Connect to the pixhawk
plane = Plane('/dev/ttyACM0')

# Create client
client = Client()

# api endpoint address
endpoint = 'http://10.110.180.122:5000/telemetry'


# while(True):
#     client.send_post(endpoint, plane.getTelemetryData())
#     time.sleep(3)


# monitor mission
nextwaypoint = plane.vehicle.commands.next
while nextwaypoint < len(plane.vehicle.commands):
    if plane.vehicle.commands.next > nextwaypoint:
        display_seq = plane.vehicle.commands.next
        #if takeoff command is added, the waypoints will be 1 off
        print("Moving to waypoint %s" % display_seq)
        nextwaypoint = display_seq
    # send Telemetry Data
    client.send_post(endpoint, plane.getTelemetryData())
    time.sleep(3)





def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    # spin runs the callback functions
    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


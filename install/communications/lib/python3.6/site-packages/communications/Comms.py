import requests
import json

class Client():

	def send_get(self, endpoint):
		return requests.get(endpoint).text
		# print(response.status_code)

		# if response.status_code == 200: #can also be written as if response:
		# 	print('Success!')
		# elif response.status_code == 404:
		# 	print('Error: Not Found')

		# response.encoding = 'utf-8'
		# print(response.text)
    

	# gets data as dictionary
	def send_post(self, endpoint, data):
		# convert to json
		post = json.dumps(data)
		# send data 
		requests.post(endpoint, post)


# import Node class
import rclpy
from rclpy.node import Node 

# import string message type 
from std_msgs.msg import String

class Comms(Node):
    def __init__(self):
        # initialize super class
        super().__init__('comms_node')
        # Create a telem subscription
        self.telem_subscriber = self.create_subscription(String, 'telem', self.telem_subscriber_callback, 10)

        # mission publisher
        self.mission_publisher = self.create_publisher(String, 'mission', 10)

        # set rate of publishing 
        self.timer_period = 1   #1 second(1Hz)
        self.mode_timer = self.create_timer(self.timer_period, self.mission_publisher_callback)

        # Create client
        self.client = Client()

        # api endpoint address
        # self.endpoint = 'http://10.110.180.122:5000/telemetry'
        self.telemetry_endpoint = 'http://192.168.50.36:5000/telemetry'
        self.mission_endpoint = 'http://192.168.50.36:5000/mission'


    def telem_subscriber_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        self.client.send_post(self.telemetry_endpoint, msg.data)

    def mission_publisher_callback(self):
        msg = String()
        msg.data = str(self.client.send_get(self.mission_endpoint))
        self.mission_publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        



# # monitor mission
# nextwaypoint = plane.vehicle.commands.next
# while nextwaypoint < len(plane.vehicle.commands):
#     if plane.vehicle.commands.next > nextwaypoint:
#         display_seq = plane.vehicle.commands.next
#         #if takeoff command is added, the waypoints will be 1 off
#         print("Moving to waypoint %s" % display_seq)
#         nextwaypoint = display_seq
#     # send Telemetry Data
#     client.send_post(endpoint, plane.getTelemetryData())
#     time.sleep(3)





def main(args=None):
    rclpy.init(args=args)

    comms = Comms()

    # spin runs the callback functions
    rclpy.spin(comms)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    Comms.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


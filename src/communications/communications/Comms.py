import requests
import json
from datetime import datetime

class Client():

	def send_get(self, endpoint):
		return requests.get(endpoint).json()
    
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
        self.kraken_subscriber = self.create_subscription(String, 'kraken', self.kraken_subscriber_callback, 10)
        self.fire_coords_subscriber = self.create_subscription(String, 'fire_coords', self.fire_coords_subscriber_callback, 10)

        # mission publisher
        self.mission_publisher = self.create_publisher(String, 'mission', 10)

        # set rate of publishing 
        self.timer_period = 1  #1 second(1Hz)
        self.mode_timer = self.create_timer(self.timer_period, self.mission_publisher_callback)

        # Create client
        self.client = Client()

        # api endpoint address for testing
        # self.endpoint = 'http://192.168.99.45:5000/telemetry'        #ayrmesh
        self.telemetry_endpoint = 'http://192.168.99.45:5000/telemetry'
        self.mission_endpoint = 'http://192.168.99.45:5000/mission'
        self.kraken_endpoint = 'http://192.168.99.45:5000/kraken'
        self.fire_coords_endpoint = 'http://192.168.99.45:5000/fire_coords'


        self.current_mission = {}

        # api endpoints GCS
        # self.telemetry_endpoint = "http://127.0.0.1:5000/api/vehicleData/MAC?db_type=vehicles"


    def telem_subscriber_callback(self, msg):
        # get current time
        now = datetime.now()

        # self.get_logger().info('I heard: "%s"' % msg.data)

        # split into list
        telem_list = msg.data.split('\n')
        # convert to dictionary
        telem_dict = {
                "lastUpdateTime": str(now),
                "altitude": telem_list[0],
                "speed": telem_list[1],
                "pitch": telem_list[2],
                "roll": telem_list[3],
                "yaw": telem_list[4],
                "mode" : telem_list[7],
                "nextWaypoint": telem_list[8],
                "latestCoordinates": {
                     "lat": telem_list[5],
                     "lon": telem_list[6]
                }
            }
            
        self.client.send_post(self.telemetry_endpoint, telem_dict)

    def kraken_subscriber_callback(self, msg):

        kraken_list = msg.data.split('\n')

        kraken_dict = {
             "confidence" : kraken_list[0],
             "lat" : kraken_list[1],
             "lon" : kraken_list[2]
        }
        self.client.send_post(self.kraken_endpoint, kraken_dict)
         
    def mission_publisher_callback(self):
        # build the msg
        msg = String()

        # returns json content 
        new_mission = self.client.send_get(self.mission_endpoint)

        if len(new_mission) == 0 or new_mission == self.current_mission:
            return 
        
        print('here')
        coordinates = new_mission['coordinates']
        # iterate and add coordinates
        for coordinate in coordinates:
             lat = coordinate['lat']
             lon = coordinate['lon']
             msg.data += f"{lat}, {lon}\n"

        self.mission_publisher.publish(msg)
        self.current_mission = new_mission
        # self.get_logger().info('Publishing: "%s"' % msg.data)

    def fire_coords_subscriber_callback(self, msg):
        # split into list
        fire_coords = msg.data.split(', ')
        # convert to dictionary
        fire_dict = {
                "lat": fire_coords[0],
                "lon": fire_coords[1],
            }
            
        self.client.send_post(self.fire_coords_endpoint, fire_dict)


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


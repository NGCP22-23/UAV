import dronekit
from DroneKitScripts import Plane 
from Communications import Client
import time

# Connect to the pixhawk
plane = Plane.Plane('/dev/ttyACM0')

# Create client
client = Client.Client()


def send_telemetry_data():
    endpoint = 'http://127.0.0.1:5000/telemetry'
    # store data in dictionary
    #data = {
        #data gets updated via listners in the Plane class upon update
        #consider sending messages at a consistent interval (1 sec?)
    #}
    #send data and enpoint to client\
    client.send_post(endpoint, plane.getTelemetryData())


for i in range(5):
    time.sleep(4)
    send_telemetry_data()

# if(command == "hiker detection"){
#     pass
# } elif(command == "payload"){

# } elif(command == "fire dection"){

# }
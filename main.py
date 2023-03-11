import dronekit
from DroneKitScripts import Plane 
from Communications import Client


# Connect to the pixhawk
plane = Plane.Plane('/dev/ttyACM0')

# Create client
client = Client.Client()


def send_telemetry_data():
    endpoint = 'http://127.0.0.1:5000/Telemetry'
    # store data in dictionary
    data = {
        "mode": plane.get_ap_mode,
    }
    #send data and enpoint to client
    client.send_post(endpoint, data)



# if(command == "hiker detection"){
#     pass
# } elif(command == "payload"){

# } elif(command == "fire dection"){

# }
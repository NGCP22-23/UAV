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
        #data gets updated via listners in the Plane class upon update
        #consider sending messages at a consistent interval (1 sec?)
        "mode": plane.get_ap_mode,
        "lat": plane.pos_lat,
        "long": plane.pos_lon,

    }
    #send data and enpoint to client
    client.send_post(endpoint, data)

    
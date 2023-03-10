import dronekit
from DroneKitScripts import Plane 
import json


# Connect to the pixhawk
plane = Plane.Plane('/dev/ttyACM0')


def get_telemetry_data():
    # store data in dictionary
    x = {
        "mode": plane.get_ap_mode,
    }
    # convert into JSON:
    y = json.dumps(x)
# 1. Connect Jetson and Pixhawk
#   - ensure connection
# 2. Change to
# 

import dronekit
import socket
import exceptions
import Plane

# plane = Plane(conection_string = '/dev/ttyACM0')
plane = Plane(conection_string = 'tcp:127.0.0.1:5760')
plane.connect()



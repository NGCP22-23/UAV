import dronekit
import socket
import exceptions

def ConnectToVehicle():
    # Connect to UDP endpoint.
    print("Connecting to pixhawk...")
    try:
	
        #dronekit.connect('/dev/ttyTHS1', baud=57600, heartbeat_timeout=15)
        #vehicle = dronekit.connect('/dev/ttyTHS1', baud= 57600, wait_ready=False)
	vehicle = dronekit.connect('/dev/ttyACM0', baud= 57600, wait_ready=True)
    # Bad TCP connection
    except socket.error:
        print('No server exists!')

    # Bad TTY connection
    except exceptions.OSError as e:
        print('No serial exists!')

    # API Error
    except dronekit.APIException:
        print('Timeout!')

    # Other error
    except:
        print('Some other error!')

    print("connected")
    return vehicle
   

def ConnectionTests(vehicle):
    #print firmware version
    print('Autopilot version: %s'%vehicle.version)
    # Use returned Vehicle object to query device state - e.g. to get the mode:
    print("Mode: %s" % vehicle.mode.name)
    # print arming status
    print ("Armed: %s" % vehicle.armed)
    


plane = ConnectToVehicle()
ConnectionTests(plane)



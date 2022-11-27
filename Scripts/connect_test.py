from dronekit import connect
import socket
import exceptions


def ConnectToVehicle():
    # Connect to UDP endpoint.

    try:
        # dronekit.connect('REPLACE_connection_string_for_your_vehicle', heartbeat_timeout=15)
        connect('/dev/ttyTHS1',baud=57600,wait_ready=True)

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


    # return vehicle
   

def ConnectionTests(vehicle):
    #print firmware version
    print('Autopilot version: %s'%vehicle.version)
    # Use returned Vehicle object to query device state - e.g. to get the mode:
    print("Mode: %s" % vehicle.mode.name)
    # print mode
    print ("Mode: %s" % vehicle.mode.name)
    # print arming status
    print ("Armed: %s" % vehicle.armed)
    

ConnectToVehicle()
# plane = ConnectToVehicle()
# ConnectionTests(plane)



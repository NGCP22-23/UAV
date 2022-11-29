from pymavlink import mavutil
import time

the_connection = mavutil.mavlink_connection('/dev/ttyTHS1', buad=57600)

the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component)

data_rate = 120 
the_connection.mav.request_data_stream_send(the_connection.target_system, the_connection.target_components, mavutil.mavlink.MAV_DATA_STREAMALL, data_rate, 1)
while True:
	msg = the_connection.recv_match(blocking=True)
	print(msg)

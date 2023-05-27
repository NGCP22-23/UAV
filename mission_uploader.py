import requests
import json
from datetime import datetime

class Client():
	def send_post(self, endpoint, waypoints):

		# convert to json
		post = json.dumps(waypoints)
		# send data 
		requests.post(endpoint, post)


waypoints = {
    "coordinates" : [
        {
            "lat": 34.04238195873398,
            "lon": -117.81411424697538,
        },
        {
            "lat": 34.04329854577586,
            "lon": -117.81539298653017
        }, 
        {
            "lat": 34.04274024693057,
            "lon": -117.81366584755779
        }, 
        {
            "lat": 34.04364554486393,
            "lon":  -117.81518474806516
        }, 
        {
            "lat":34.04313769599379,
            "lon": -117.81335940271858
        }, 
        {
            "lat": 34.04406368166445,
            "lon": -117.81455317466148
        }, 
        {
            "lat": 34.043343890954105,
            "lon": -117.81308056937189
        }, 
    ],
}

endpoint = 'http://192.168.0.100:5000/mission'
mission_sender = Client()

print('Sending new mission')
mission_sender.send_post(endpoint, waypoints)

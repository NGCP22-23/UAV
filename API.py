
import json
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/telemetry', methods = ['POST'])
def telemetry():
    # convert to dictionary to iterate
    dictionary = json.loads(request.data)
    
    print('\n')
    for key in dictionary:
        print(key, " : ", dictionary[key])
    print('\n \n')

    return "success"


@app.route('/kraken', methods = ['POST'])
def kraken():
    # convert to dictionary to iterate
    dictionary = json.loads(request.data)
    
    print('\n')
    for key in dictionary:
        print(key, " : ", dictionary[key])
    print('\n \n')

    return "success"


@app.route('/mission', methods = ['GET'])
def mission():
    # example waypoints from gcs
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
    return jsonify(waypoints)


app.run(host="0.0.0.0")

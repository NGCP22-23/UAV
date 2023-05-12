
import json
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/telemetry', methods = ['POST'])
def telemetry():
    # convert to dictionary to iterate
    dictionary = json.loads(request.data)
    for key in dictionary:
        print(key, " : ", dictionary[key])
    print('\n \n')
    return "success"

@app.route('/mission', methods = ['GET'])
def mission():
    waypoints_500ft = [[34.04238195873398, -117.81411424697538], [34.04329854577586, -117.81539298653017],[34.04274024693057, -117.81366584755779],[34.04364554486393, -117.81518474806516], [34.04313769599379, -117.81335940271858], [34.04406368166445, -117.81455317466148], [34.043343890954105, -117.81308056937189] ]
    return jsonify(waypoints_500ft)


app.run(host="0.0.0.0")

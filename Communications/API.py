
import json
from flask import Flask, jsonify, request
from Autonomous.Plane import Plane
import sys


# parent directory
sys.path.append("..")

app = Flask(__name__)



@app.route('/telemetry', methods = ['POST'])
def telemetry():
    # convert to dictionary to iterate
    dictionary = json.loads(request.data)
    for key in dictionary:
        print(key, " : ", dictionary[key])
    print('\n \n')
    return "success"

@app.route('/mission_change', methods = ['POST'])
def mission_change():
    pass


app.run(host="0.0.0.0")

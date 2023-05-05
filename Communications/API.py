
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

app.run(host="0.0.0.0")

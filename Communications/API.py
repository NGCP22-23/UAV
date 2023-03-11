# from flask import Flask
# from flask_restful import Resource, Api, reqparse


# app = Flask(__name__)
# api = Api(app)


# class Telemetry(Resource):
#     def get(self):
#         return {'mode': "poop"}
#     def post(self):
#         return {'mode': ""}

# api.add_resource(Telemetry, '/Telemetry')

# if __name__ == '__main__':
#     app.run()

import json
from flask import Flask, jsonify

app = Flask(__name__)



@app.route('/telemetry', methods = ['POST'])
def telemetry(data):
    x = json.loads(data)
    print(x)

app.run()
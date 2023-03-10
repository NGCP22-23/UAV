from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)


class Telementry(Resource):
    def get(self):
        return {'mode': "poop"}
    def post(self):
        return {'mode'}

api.add_resource(Telemetry, '/Telemetry')

if __name__ == '__main__':
    app.run()
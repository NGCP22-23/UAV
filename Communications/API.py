from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)


class UAV(Resource):
    def get(self):
        return {'data': "poop"}

api.add_resource(UAV, '/UAV')

if __name__ == '__main__':
    app.run()
import json
from flask import Flask, jsonify, request

class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.waypoints = {}

        # Add any additional initialization code here

    def telemetry(self):
        # convert to dictionary to iterate
        dictionary = json.loads(request.data)

        print('\n')
        for key in dictionary:
            print(key, " : ", dictionary[key])
        print('\n \n')

        return "success"

    def kraken(self):
        # convert to dictionary to iterate
        dictionary = json.loads(request.data)

        print('\n')
        for key in dictionary:
            print(key, " : ", dictionary[key])
        print('\n \n')
        return "success"

    def post_mission(self):
        self.waypoints = json.loads(request.data)
        return "mission uploaded to API"

    def get_mission(self):
        return jsonify(self.waypoints)


app = MyApp(__name__)

# Define your routes
app.add_url_rule('/telemetry', view_func=app.telemetry, methods=['POST'])
app.add_url_rule('/kraken', view_func=app.kraken, methods=['POST'])
app.add_url_rule('/mission', view_func=app.post_mission, methods=['POST'])
app.add_url_rule('/mission', view_func=app.get_mission, methods=['GET'])

if __name__ == '__main__':
    app.run(host="0.0.0.0")

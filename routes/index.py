from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask_cors import CORS
from services.CameraPositions import CameraPositions


def create_app():
    app = Flask(__name__)
    return app


app = create_app()
CORS(app)


@app.errorhandler(400)
def bad_request(e):
    return "<h1>Bad Request</h1>", 400


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>Url not found</h1>", 404


@app.route('/', methods=['POST'])
def find_camera_positions():
    req = request.get_json()
    cameras = req["numberSensors"]
    radio = req["radius"]
    data = req["data"]
    camera_positions = CameraPositions(cameras, radio, data)
    response = camera_positions.run()
    res = make_response(jsonify(response), 201)
    return res

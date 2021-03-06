#!/usr/bin/python3
""" first part of the restful api """
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import environ
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_request(exception=None):
    """ a method to call close() """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ doc for not_found error """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host1 = environ.get("HBNB_API_HOST")
    port1 = environ.get("HBNB_API_PORT")
    app.run(host=host1, port=port1, threaded=True)

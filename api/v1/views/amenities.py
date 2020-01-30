#!/usr/bin/python3
""" doc for amenities.py module """
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"])
def get_amenities():
    """ doc for get_amenities method """
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """ doc for get_amenity """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """ doc for delete_amenity method """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'])
def create_amenity():
    """ doc for create_amenity method """
    amenity_new = request.get_json()
    if not amenity_new:
        abort(400, "Not a JSON")
    if 'name' not in amenity_new:
        abort(400, "Missing name")
    amenity = Amenity(**amenity_new)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id):
    """ doc for update_amenity """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    b_req = request.get_json()
    if not b_req:
        abort(400, "Not a JSON")
    for key, value in b_req.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)

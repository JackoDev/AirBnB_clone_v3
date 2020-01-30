#!/usr/bin/python3
""" doc for cities.py module """
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=["GET"])
def get_cities(state_id):
    """ doc for get_cities method """
    state=storage.get("State",state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """ doc for get_city """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """ doc for delete_city method """
    city = storage.get("City", id=city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def create_city(state_id):
    """ doc for create_city method """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    city_new = request.get_json()
    if not city_new:
        abort(400, "Not a JSON")
    if 'name' not in city_new:
        abort(400, "Missing name")
    city = City(**city_new)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    """ doc for update_city """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    b_req = request.get_json()
    if not b_req:
        abort(400, "Not a JSON")
    for key, value in b_req.items():
        if key != 'id' and key != 'state_id' and key != 'created_at'
        and key != 'updated_at':
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)

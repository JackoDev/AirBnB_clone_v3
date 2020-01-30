#!/usr/bin/python3
""" doc for states.py module """
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/states')
def get_states():
    """ doc for get_states method """
    list_states = []
    for s in storage.all("State").values():
        list_states.append(s.to_dict())
    return jsonify(list_states)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """ doc for get_state """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """ doc for delete_state method """
    state = storage.get("State", id=state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'])
def create_state():
    """ doc for create_state method """
    state_new = request.get_json()
    if not state_new:
        abort(400, "Not a JSON")
    if 'name' not in state_new:
        abort(400, "Missing name")
    state = State(**state_new)
    storage.new(state)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    """ doc for update_state """"
    state = storage.get("State", id=state_id)
    if not state:
        abort(404)
    b_req = request.get_json()
    if not b_req:
        abort(400, "Not a JSON")
    for key, value in b_req.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)

#!/usr/bin/python3
""" doc for users.py module """
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=["GET"])
def get_users():
    """ doc for get_users method """
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """ doc for get_user """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """ doc for delete_user method """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'])
def create_user():
    """ doc for create_user method """
    user_new = request.get_json()
    if not user_new:
        abort(400, "Not a JSON")
    if 'name' not in user_new:
        abort(400, "Missing name")
    user = User(**user_new)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    """ doc for update_user method """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    b_req = request.get_json()
    if not b_req:
        abort(400, "Not a JSON")
    for key, value in b_req.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

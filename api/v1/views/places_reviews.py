#!/usr/bin/python3
"""
Places review
"""

import models
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views

@app_views.route('places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Create and returns a new review with the status code 201
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'text' not in request.json:
        abort(400, "Missing text")
    place = storage.get("Place", place_id)
    user = storage.get("User", id=request.json['user_id'])
    if place and user:
        request.json['place_id'] = place_id
        review = models.review.Review(**request.json)
        review.save()
        return jsonify(review.to_dict()), 201
    abort(404)
    
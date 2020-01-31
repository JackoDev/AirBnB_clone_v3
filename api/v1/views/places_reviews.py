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
    
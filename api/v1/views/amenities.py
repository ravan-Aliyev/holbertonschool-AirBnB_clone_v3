#!/usr/bin/python3
"""Amenity api"""
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def retrive_all_amenity():
    """Get all amenities"""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def retrive_amenity(amenity_id):
    """Get amenity by id"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        return jsonify(amenity.to_dict())
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if (amenity is None):
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Create amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")

    amenity = Amenity(**request.get_json())

    if amenity.name is None:
        abort(400, "Missing name")

    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """Update amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)

    amenity.save()

    return jsonify(amenity.to_dict())

#!/usr/bin/python3
"""Place api"""
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def retrive_all_place(city_id):
    """Get all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def retrive_place(place_id):
    """Get place by id"""
    try:
        place = storage.get(Place, place_id)
        return jsonify(place.to_dict())
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Delete place"""
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Create place"""
    if not request.is_json:
        abort(400, "Not a JSON")

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place = Place(**request.get_json())

    if place.user_id is None:
        abort(400, "Missing user_id")
    if place.name is None:
        abort(400, "Missing name")

    user = storage.get(User, place.user_id)

    if user is None:
        abort(404)

    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Update place"""
    if not request.is_json:
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(place, k, v)

    place.save()

    return jsonify(place.to_dict())

#!/usr/bin/python3
"""City api"""
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def retrive_all_cities(state_id):
    """Get all cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def retrive_city(city_id):
    """Get city by id"""
    try:
        city = storage.get(City, city_id)
        return jsonify(city.to_dict())
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Delete city by id"""
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Create city"""
    if not request.is_json:
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    city = City(**request.get_json())

    if city.name is None:
        abort(400, "Missing name")

    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Update city"""
    if not request.is_json:
        abort(400, "Not a JSON")

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, k, v)

    city.save()

    return jsonify(city.to_dict())

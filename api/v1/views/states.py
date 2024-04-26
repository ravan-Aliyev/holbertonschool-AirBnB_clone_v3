#!/usr/bin/python3
"""
States api
"""
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states', strict_slashes=False)
def retrive_all():
    """Getting all states"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def retrive(state_id):
    """Get state by id"""
    try:
        state = storage.get(State, state_id)
        return jsonify(state.to_dict())
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete(state_id):
    """Delete state"""
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create():
    """Create state"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = State(**request.get_json())

    if data.name is None:
        abort(400, "Missing name")

    data.save()
    return jsonify(data.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update(state_id):
    """Update state"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = storage.get(State, state_id)

    if data is None:
        abort(404)

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(data, k, v)

    data.save()

    return jsonify(data.to_dict())

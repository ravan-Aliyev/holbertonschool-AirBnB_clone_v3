#!/usr/bin/python3
"""User api"""
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def retrive_all_user():
    """Get all users"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def retrive_user(user_id):
    """Get user by id"""
    try:
        user = storage.get(User, user_id)
        return jsonify(user.to_dict())
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    user = storage.get(User, user_id)
    if (user is None):
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Create user"""
    if not request.is_json:
        abort(400, "Not a JSON")

    user = User(**request.get_json())

    if user.email is None:
        abort(400, "Missing email")
    if user.password is None:
        abort(400, "Missing password")

    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Update user"""
    if not request.is_json:
        abort(400, "Not a JSON")

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, k, v)

    user.save()

    return jsonify(user.to_dict())

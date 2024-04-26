#!/usr/bin/python3
"""Review api"""
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def retrive_all_review(place_id):
    """Get all review"""
    place = storage.get(Review, place_id)
    if place is None:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(place.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def retrive_review(review_id):
    """Get review by id"""
    try:
        review = storage.get(Review, review_id)
        return jsonify(review.to_dict())
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Delete review"""
    review = storage.get(Review, review_id)
    if (review is None):
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """Create review"""
    if not request.is_json:
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    review = Review(**request.get_json())

    if review.user_id is None:
        abort(400, "Missing user_id")
    if review.text is None:
        abort(400, "Missing text")

    user = storage.get(User, review.user_id)

    if user is None:
        abort(404)

    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Update review"""
    if not request.is_json:
        abort(400, "Not a JSON")

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(review, k, v)

    review.save()

    return jsonify(review.to_dict())

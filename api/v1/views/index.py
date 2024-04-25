#!/usr/bin/python3
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    data = {
        'status': "OK"
    }
    return jsonify(data)


@app_views.route('/stats')
def stats():
    data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(data)

#!/usr/bin/python3
"""
API
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """Close session"""
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """For 404 errors"""
    data = {
        "error": "Not found"
    }
    return jsonify(data), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)

#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states_list: HTML page with a list of all State objects in DBStorage.
"""
from flask import Flask, render_template
from models import storage

app = Flask("__name__", template_folder="web_flask/templates")


@app.route("/states_list", strict_slashes=False)
def get_States():
    """Displays an HTML page with a list of all State objects in DBStorage.

    States are sorted by name.
    """
    return render_template("7-states_list.html", states=storage.all("State"))


@app.teardown_appcontext
def close_storage(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

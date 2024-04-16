#!/usr/bin/python3
from flask import Flask, render_template
from models import storage

app = Flask("__name__", template_folder="web_flask/templates")


@app.route("/states_list", strict_slashes=False)
def get_States():
    return render_template("7-states_list.html", states=storage.all("State"))


@app.teardown_appcontext
def close_storage(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

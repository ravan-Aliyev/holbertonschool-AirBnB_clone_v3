from flask import Blueprint

app_views = Blueprint(name="index", import_name=__name__, url_prefix='/api/v1')

if app_views is not None:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
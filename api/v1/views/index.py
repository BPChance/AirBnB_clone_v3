#!/usr/bin/python3
""" create an endpoint """
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

model_classes = {"amenities": Amenity, "cities": City,
                 "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'])
def get_status():
    """ returns api status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def get_stats():
    """ return counts of different objects """
    return_dict = {}
    for object in model_classes:
        object_dict = {object: storage.count(model_classes[object])}
        return_dict.update(object_dict)
    return jsonify(return_dict)

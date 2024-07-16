#!/usr/bin/python3
""" cities objects view """

from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """ gets the list of all cities objects """
    cities = storage.all(City).values()
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrieves a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ delete a city object """
    city = storage.get(City, city_id)
    abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """ creates a city """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_city = City(**data)
    new_city.state_id = state.id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
    return jsonify(state.to_dict()), 200

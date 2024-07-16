#!/usr/bin/python3
""" users objects view """

from flask import jsonify, request, abort
from models import storage
from models.user import User  
from api.v1.views import app_views


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_users():
    """ gets the list of all users objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ retrieves a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ deletes a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_user():
    """ creates a user """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    try:
        storage.save()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        abort(500, description="Internal server error: {}".format(e))

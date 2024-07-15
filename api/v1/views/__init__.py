#!/usr/bin/python3
""" set up the blueprint """

from flask import Blueprint

app_views = Blueprint

from api.v1.views.index import *

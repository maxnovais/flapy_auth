# coding: utf-8
"""The views of user administration are here"""
from flask import Blueprint


blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

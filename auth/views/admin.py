# coding: utf-8
from flask import Blueprint

blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# coding: utf-8
from collections import OrderedDict
from functools import wraps
from flask import request, abort
from flask_login import current_user
from datetime import datetime
from auth.models import User, Role
from auth.exceptions import RoleNotFound


def login_permission(permission):
    """Check if current_user has a permission to see"""
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = User.query.get(current_user.get_id())
            try:
                role = Role.search_role(permission, True)
                if user.has_role(role):
                    return function(*args, **kwargs)
            except RoleNotFound:
                return abort(403)
            return abort(403)
        return wrapper
    return decorator


def dict_object(query_object):
    result = OrderedDict()
    for key in query_object.__mapper__.c.keys():
        result[key] = getattr(query_object, key)

        if isinstance(result[key], datetime):
            result[key] = getattr(query_object, key).strftime('%d/%m/%Y %H:%M:%S')
    return result


def dict_list(query):
    list = []
    for query_object in query:
        list.append(dict_object(query_object))
    return list


def query_object_list(model, paginable=True):
    if paginable:
        # Get Request Args from get /?limit=10&offset=0
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0,  type=int)
    else:
        limit = 10
        offset = 0

    query = model.query
    count = query.fast_count()
    data = dict_list(query.order_by(model.id.desc()).limit(limit).offset(offset).all())
    return data, count

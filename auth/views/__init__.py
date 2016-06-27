# coding: utf-8
from collections import OrderedDict
from flask_login import current_user
from datetime import datetime
from auth.models import User, Role
from auth.exceptions import RoleNotFound


def login_permission(permissions):
    """Check if current_user has a permission to see"""
    user = User.query.get(current_user.get_id())
    for permission in permissions:
        try:
            role = Role.search_role(permission, True)
        except RoleNotFound:
            return False
        if user.has_role(role):
            return True
    return False


def dict_list(query):
    list = []
    for object in query:
        result = OrderedDict()
        for key in object.__mapper__.c.keys():
            result[key] = getattr(object, key)

            if isinstance(result[key], datetime):
                result[key] = getattr(object, key).strftime('%d/%m/%Y %H:%M:%S')
        list.append(result)
    return list

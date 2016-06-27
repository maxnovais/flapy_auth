# coding: utf-8
from flask_login import current_user
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

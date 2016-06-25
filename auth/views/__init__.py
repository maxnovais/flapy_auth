# coding: utf-8
from flask_login import current_user
from auth.exceptions import RoleNotFound


def login_permission(permissions):
    user = UserAction.get_by_id(current_user.get_id())
    for permission in permissions:
        try:
            role = RoleAction.search_role(name=permission, exactly=True)
        except RoleNotFound:
            return False
        if UserRoleAction.user_has_role(user, role):
            return True
    return False

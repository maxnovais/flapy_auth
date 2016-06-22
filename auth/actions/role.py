# coding: utf-8
from sqlalchemy.exc import IntegrityError
from auth.exceptions import InvalidRoleName, RoleAlreadyExist, RoleNotFound
from auth.models import Role


class RoleAction(object):
    @staticmethod
    def create(name, description=None):
        if len(name) < 3:
            raise InvalidRoleName

        try:
            role = Role()
            role.name = name
            role.description = description
            role.save(commit=True)
            return role
        except IntegrityError:
            raise RoleAlreadyExist

    @staticmethod
    def edit(role_id, name=None, description=None):
        try:
            role = Role.query.get(role_id)
            if name:
                if len(name) < 3:
                    raise InvalidRoleName
                role.name = name
            if description:
                role.description = description
            role.save(commit=True)
        except IntegrityError:
            raise RoleAlreadyExist
        return role

    @staticmethod
    def delete(role_id):
        role = Role.query.get(role_id)
        role.delete(commit=True)

    @staticmethod
    def change_status(role_id):
        role = Role.query.get(role_id)
        if role.active:
            role.active = False
        else:
            role.active = True
        role.save(commit=True)

    @staticmethod
    def search_role(name, exactly=False):
        role = Role()
        if exactly:
            role = role.query.filter(Role.name == name).first()
        else:
            role = role.query.filter(Role.name.contains(name)).all()
        if not role:
            raise RoleNotFound
        return role



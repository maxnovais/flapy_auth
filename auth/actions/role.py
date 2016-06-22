# coding: utf-8
from sqlalchemy.exc import IntegrityError
from auth.exceptions import RoleAlreadyExist, RoleNotFound
from auth.models import Role


class RoleAction(object):
    @staticmethod
    def create(name, description=None):
        try:
            role = Role()
            role.name = name
            role.description = description
            role.save(commit=True)
            return role
        except IntegrityError:
            raise RoleAlreadyExist

    @staticmethod
    def edit(role_id, new_name, new_description):
        role = Role.query.get(role_id)
        if new_name:
            role.name = new_name
        if new_description:
            role.description = new_description
        role.save(commit=True)
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
    def search_role_by_exactly_name(name, exactly=False):
        role = Role()
        if exactly:
            role = role.query.filter(Role.name == name).first()
        else:
            role = role.query.filter(Role.name.contains(name)).all()
        if not role:
            raise RoleNotFound
        return role



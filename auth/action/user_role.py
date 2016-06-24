# coding: utf-8
from sqlalchemy.exc import IntegrityError
from auth.exceptions import RoleAlreadyEmpty, UserNotHasRole, UserAlreadyInRole
from auth.models import UserRole, db


class UserRoleAction(object):
    @staticmethod
    def set_role(user, role):
        try:
            user_role = UserRole()
            user_role.user_id = user.id
            user_role.role_id = role.id
            user_role.save()
            db.session.commit()
        except IntegrityError:
            raise UserAlreadyInRole

    @staticmethod
    def get_role(user, role):
        return UserRole.query.filter(UserRole.user_id == user.id, UserRole.role_id == role.id).one()

    def delete_role(self, user, role):
        user_role = self.get_role(user, role)
        user_role.delete()
        db.session.commit()

    @staticmethod
    def get_user_roles(user):
        return UserRole.query.filter(UserRole.user == user).all()

    def get_roles(self, user):
        user_roles = self.get_user_roles(user)
        roles = []
        for user_role in user_roles:
            roles.append(user_role.role)
        return roles

    @staticmethod
    def get_users_in_role(role):
        return UserRole.query.filter(UserRole.role == role).all()

    def get_users(self, role):
        user_roles = self.get_users_in_role(role)
        users = []
        for user_role in user_roles:
            users.append(user_role.user)
        return users

    def empty_role(self, role):
        users_roles = self.get_users_in_role(role)
        if len(users_roles) == 0:
            raise RoleAlreadyEmpty
        for user_role in users_roles:
            self.delete_role(user_role.user, user_role.role)

    def remove_user_roles(self, user):
        users_roles = self.get_user_roles(user)
        if len(users_roles) == 0:
            raise UserNotHasRole
        for user_role in users_roles:
            self.delete_role(user_role.user, user_role.role)

    def user_has_role(self, user, role):
        user_roles = self.get_roles(user)
        if role in user_roles:
            return True
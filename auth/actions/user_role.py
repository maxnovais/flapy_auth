# coding: utf-8
from auth.models import User, Role, UserRole


class UserRoleAction(object):

    def set_role(self, user, role):
        user_role = UserRole()
        user_role.user_id = user.id
        user_role.role_id = role.id
        user_role.save(commit=True)

    def get_role(self, user, role):
        return UserRole.query.filter(UserRole.user_id == user.id, UserRole.role_id == role.id).one()

    def delete_role(self, user, role):
        user_role = self.get_role(user, role)
        user_role.delete()


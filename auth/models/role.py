# coding: utf-8
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from auth.exceptions import InvalidRoleName, RoleAlreadyExist, RoleNotFound
from auth.models import Model, db


class Role(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())

    @property
    def is_active(self):
        """Return current status of role"""
        return self.active

    @classmethod
    def create(cls, name, description=None):
        """Create new role"""
        if len(name) < 3:
            raise InvalidRoleName

        try:
            role = Role()
            role.name = name
            role.description = description
            role.save()
            db.session.commit()
            return role
        except IntegrityError:
            raise RoleAlreadyExist

    def edit(self, name=None, description=None):
        """Edit existent role"""
        try:
            if name:
                if len(name) < 3:
                    raise InvalidRoleName
                self.name = name
            if description:
                self.description = description
            self.save()
            db.session.commit()
        except IntegrityError:
            raise RoleAlreadyExist
        return self

    @classmethod
    def search_role(cls, name, exactly=False):
        """Search role by name, exactly or not"""
        if exactly:
            role = cls.query.filter(Role.name == name).all()
        else:
            role = cls.query.filter(Role.name.contains(name)).all()
        if not role:
            raise RoleNotFound
        return role

    @property
    def users(self):
        """Return all users in this role"""
        users = []
        for role_user in self.role_users:
            users.append(role_user.user)
        return users

    def remove_all_users(self):
        """Remove all users in this role"""
        for role_user in self.role_users:
            role_user.delete(commit=True)
        db.session.commit()

# coding: utf-8
from datetime import datetime
from auth.models import Model, db, User, Role


class UserRole(Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user_role'

    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User", backref="user_roles")
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    role = db.relationship("Role")

    __table_args__ = (db.UniqueConstraint('user_id', 'role_id', name='un_user_role'),)

# coding: utf-8
from collections import OrderedDict
import datetime

from flask_sqlalchemy import models_committed, BaseQuery
from sqlalchemy import func

from auth.exceptions import ValidationError, SessionNotFound
from auth.main import db


@models_committed.connect
def models_committed_handler(sender, **kwrags):
    """
    Mark the instance as _new = True for just created object otherwise as False
    """
    for obj, action in kwrags['changes']:
        if action == 'insert':
            obj._new = True


class ModelMixin(object):
    _new = False

    patchable = ()
    unpatchable = ()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.flush()

    def refresh(self):
        if not self._sa_instance_state.session:
            raise SessionNotFound("You can't refresh an object that has no session.")

        self._sa_instance_state.session.refresh(self)

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.flush()

    def _asdict(self):
        """This method is called by JSON dumps
        """
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)

            if isinstance(result[key], datetime.datetime):
                result[key] = getattr(self, key).strftime('%d/%m/%Y %H:%M:%S')

        return result

    def __repr__(self):
        field = value = None
        for f in ('name', 'username', 'created', 'uuid'):
            if hasattr(self, f):
                field = f
                value = getattr(self, f)
                break
        if field:
            return "<{name}[{id!r}] {field}={value!r}>".format(
                name=self.__class__.__name__, id=self.id, field=field, value=value)
        else:
            return "<{name}[{id!r}]>".format(
                name=self.__class__.__name__, id=self.id)

    def toggle_status(self):
        if self.active:
            self.active = False
        else:
            self.active = True
        self.save()
        db.session.commit()


class Query(BaseQuery):
    def fast_count(self):
        """For complicated reasons, SQLAlchemy doesn't do a `count(*)` when
        you call `query.count()`. Instead, it retrieves the whole resultset in a
        subquery and runs the `count('*')` on it, which is terribly slow
        sometimes.
        This method converts the select clause of the query to a single
        `func.count('*')` statement, allowing for much faster count.
        """

        counter = self.with_entities(func.count('*'))

        if counter.whereclause is None:
            counter = counter.select_from(self._entities[0].type)

        return counter.scalar()


class Model(db.Model, ModelMixin):
    __abstract__ = True
    query_class = Query


from auth.models.user import User #NSQA
from auth.models.role import Role #NSQA
from auth.models.user_role import UserRole #NSQA

from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
import hashlib, os
from datetime import datetime

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

class RolesUsers(db.Model):

    id = Column(db.Integer(), primary_key=True)
    user_id = Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    role_id = Column(db.Integer(), db.ForeignKey('role.id'), nullable=False)
    expires_at = Column(db.DateTime)
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id'),
    )
    user = relationship('User', backref=db.backref('roles_user', lazy='dynamic', cascade="all,delete-orphan"))
    role = relationship('Role', backref=db.backref('users_role', lazy='dynamic', cascade="all,delete-orphan"))


class Role(db.Model, RoleMixin):

    id = Column(db.Integer(), primary_key=True)
    name = Column(db.VARCHAR(80), unique=True)
    description = Column(db.String(255))

    def __repr__(self):
        return f'{self.name}'

    @classmethod
    def get_role_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def __hash__(self):
        return hash(self.name)

class User(db.Model, UserMixin):

    id = Column(db.INTEGER(), nullable=False, primary_key=True)
    username = Column(db.VARCHAR(length=50), nullable=False, unique=True)
    email = Column(db.VARCHAR())
    password = Column(db.VARCHAR(length=255))
    active = Column(db.Boolean(), server_default='t', default=True)
    roles = relationship('Role', secondary="roles_users",
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"{type(self).__name__} <{self.username}>"

    def has_role(self, *roles):
        if len(roles) > 1:
            return self._has_any_role(*roles)
        else:
            return super().has_role(*roles)

    def _has_any_role(self, *roles):
        return any([self.has_role(role) for role in roles])

    def check_role_time(self, role):
        if isinstance(role, str):
            roles_users = [role_user for role_user in self.roles_user if role_user.role.name == role and
                           (
                               (role_user.expires_at is None) or
                               (role_user.expires_at > datetime.now())
                           )
                           ]
        else:
            roles_users = [role_user for role_user in self.roles_user if role_user.role == role and
                           (
                               (role_user.expires_at is None) or
                               (role_user.expires_at > datetime.now())
                           )
                           ]
        if roles_users:
            return True
        return False

    def set_token(self):
        new_token = User.make_hash()
        self.token = new_token
        return new_token

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if self.password:
            return check_password_hash(self.password, password)

    @classmethod
    def register_user(cls, username, password, email):
        user = cls(username = username, email = email)
        user.set_password(password)
        user.save_to_db()

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def make_hash():
        return hashlib.md5(os.urandom(100)).hexdigest()
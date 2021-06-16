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
    description = Column(db.VARCHAR(255))

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
    email = Column(db.VARCHAR(length=255), nullable=False, unique=True)
    password = Column(db.VARCHAR(length=255), nullable=False)
    weak_token = Column(db.VARCHAR(length=255))
    active = Column(db.Boolean(), server_default='t', default=True)
    posts = relationship('Post', backref='users', cascade="all,delete-orphan")
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

    def set_weak_token(self):
        new_token = User.make_weak_hash(self.username)
        self.weak_token = new_token
        return new_token

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = password
        # self.password = generate_password_hash(password)

    def check_password(self, password):
        # if self.password:
        #     return check_password_hash(self.password, password)
        return password == self.password

    def to_list(self):
        fields =  [getattr(self, c.name) for c in self.__table__.columns]
        return fields

    def to_dict(self):
        fields =  {c.name : getattr(self, c.name) for c in self.__table__.columns}
        return fields

    @classmethod
    def register_user(cls, username, password, email, role_name = None):
        user = cls(username = username, email = email)
        user.set_password(password)
        user.set_weak_token()
        if role_name:
            role = Role.get_role_by_name(role_name)
            user.roles.append(role)
        user.save_to_db()
        return user

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_weak_hash(cls, hash):
        return cls.query.filter_by(weak_token=hash).first()

    @staticmethod
    def make_weak_hash(data):
        return hashlib.md5(data.encode()).hexdigest()


class Post(db.Model):

    id = Column(db.INTEGER(), nullable=False, primary_key=True)
    user_id = Column(db.Integer(), db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    author = Column(db.TEXT(), nullable=False)
    text = Column(db.TEXT(), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self, ignore = None):
        ignore = ignore or ["id"]
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ignore}

    @classmethod
    def register_post(cls, author, text):
        post = Post(
            author = author,
            text = text
        )
        post.save_to_db()

    @classmethod
    def get_all(cls):
        posts = Post.query.all()
        return [post.to_json() for post in posts]

    @classmethod
    def remove_all_by_user_id(cls, user_id):
        posts = Post.query.filter_by(user_id = user_id)
        posts.delete()
        db.session.commit()
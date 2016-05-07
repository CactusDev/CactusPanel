from app import app, db
from passlib.context import CryptContext
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask.ext.security import (Security, SQLAlchemyUserDatastore,
                                UserMixin, RoleMixin)

pwd_context = CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256", "des_crypt"],
    default="bcrypt",
    all__vary_rounds=0.1
)

roles_users = db.Table('roles_users',
                       db.Column('user_id',
                                 db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id',
                                 db.Integer(),
                                 db.ForeignKey('role.id'))
                       )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(120), index=True, unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    provider_id = db.Column(db.String(64), index=True, unique=True)
    # Creates a link to all Bot models created backref-ing this User model
    bots = db.relationship("Bot", backref="b_owner")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id)

    def hash_password(self, password):
        self.hashed_password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def gen_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            # valid token, but expired
            return None
        except BadSignature:
            # invalid token
            return None
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<{name} - [{id}] {owner}>".format(
            name=self.name,
            id=self.id,
            owner=self.owner
        )


class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who = db.Column(db.String(1000), index=True)
    issue = db.Column(db.String(1000))
    details = db.Column(db.String(10000))
    been_read = db.Column(db.Boolean, default=False)
    representative = db.Column(db.String(100), default="")

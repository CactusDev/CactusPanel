"""
RethinkDB models for remodel
"""

from remodel.models import Model

roles_users = db.Table('roles_users',
                       db.Column('user_id',
                                 db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id',
                                 db.Integer(),
                                 db.ForeignKey('role.id'))
                       )

class User(Model):
    """
    A remodel table model
    """

    def get_id(self):
        """
        Returns a string of the User object's ID
        """
        return str(self["id"])

    @property
    def is_active(self):
        """
        Returns a string of the User object's ID
        """
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return True


class Roles(Model):
    """
    A remodel table model
    """
    pass

    def gen_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

class Channels(Model):
    """
    A remodel table model
    """
    pass

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Configuration(Model):
    """
    A remodel table model
    """
    pass

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Commands(Model):
    """
    A remodel table model
    """
    pass

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

class Messages(Model):
    """
    A remodel table model
    """
    pass


class Executions(Model):
    """
    A remodel table model
    """
    pass


class Quotes(Model):
    """
    A remodel table model
    """
    pass


class UserRole(Model):
    """
    A remodel table model
    """
    pass


class Tickets(Model):
    """
    A remodel table model
    """
    pass


class TicketResponse(Model):
    """
    A remodel table model
    """
    pass

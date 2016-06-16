"""
Initializes the RethinkDB with the tables we need
Simply add a new class as needed to create new tables

The MIT License (MIT)

Copyright (c) RPiAwesomeness 2016

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from remodel.models import Model
import remodel.helpers
import remodel.connection
import rethinkdb as rethink
from rethinkdb.errors import ReqlDriverError

try:
    conn = rethink.connect("localhost", 28015)
except ReqlDriverError as error:
    print("Failed to connect to database at 'localhost:28015'!")
    print(error)
    raise SystemExit

if not rethink.db_list().contains("cactus").run(conn):
    rethink.db_create("cactus").run(conn)
    print("Database successfully created!")

remodel.connection.pool.configure(db="cactus")


class User(Model):
    """
    A remodel table model
    """
    def get_id(self):
        """
        Returns a string of the User object's ID
        """
        return str(self['id'])


class Roles(Model):
    """
    A remodel table model
    """
    pass


class Channels(Model):
    """
    A remodel table model
    """
    pass


class Configuration(Model):
    """
    A remodel table model
    """
    pass


class Commands(Model):
    """
    A remodel table model
    """
    pass


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

remodel.helpers.create_tables()
remodel.helpers.create_indexes()

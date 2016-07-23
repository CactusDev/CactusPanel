"""Create a new rethink database."""

import remodel.helpers
import remodel.connection
import rethinkdb as rethink
from rethinkdb.errors import ReqlDriverError
from app.models import *

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

remodel.helpers.create_tables()
remodel.helpers.create_indexes()

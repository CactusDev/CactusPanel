"""
Provides ticket endpoints and controls for Cactus-CP
"""

import json
from functools import partial
from uuid import uuid4
import rethinkdb as rethink
import jrpc_helper as jrpc
from flask import jsonify, session
from flask_login import request, login_required
from werkzeug import ImmutableMultiDict
from ..models import Tickets
from .. import app, csrf_protect


@csrf_protect.exempt
@login_required
@app.route("/support", methods=["POST"])
def support_router():
    """
    Provides the JSON-RPC endpoint for tickets
    """

    if request.method == "POST":

        if request.get_json() is not None:
            # We'll go with what comes through JSON
            data = request.get_json()
        elif request.args != ImmutableMultiDict():
            data = request.args
        else:
            data = request.data.decode("utf-8")

        if data == "":
            error_packet = jrpc.JSONRPCError(
                code=-32600,
                message="Invalid Request",
                data="No data was provided in POST request. POST must "
                     "include JSON-RPC compliant JSON data",
                response_id=None        # Required to be JSON-RPC compliant
            ).packet

            return jsonify(error_packet)

        methods = {
            "retrieve:newest": partial(list_tickets, data),
            "retrieve:search": partial(list_tickets, data),
            "create": partial(create_ticket, data),
            # "respond": partial(respond_to_ticket, data)
        }

        return_data = json.loads(methods[data["method"]]())

        response_packet = jrpc.JSONRPCResult(
            response_id=data["id"] if "id" in data else None,
            result={"results": return_data},
        ).packet

        print(response_packet)

        return jsonify(response_packet)

    else:                          # Not GET/POST (somehow), method not allowed
        error_packet = jrpc.JSONRPCError(
            code=405,
            message="Method not allowed",
            data="Method {} is not allowed on this endpoint".format(
                request.method),
            response_id=None            # Required to be JSON-RPC compliant
        ).packet
        return jsonify(error_packet)


@login_required
@app.route("/support/create", methods=["GET"])
def create_ticket_directive():
    if request.method == "GET":
        return render_template("partials/CreateSupportTicket.html")
    else:
        return "Method not allowed"


@login_required
@app.route("/support/respond", methods=["GET"])
def respond_ticket_directive():
    if request.method == "GET":
        return render_template("directives/RespondToTicket.html")
    else:
        return "Method not allowed"


def create_ticket(packet):
    """
    Creates and returns a new ticket
    """

    params = packet["params"]

    ticket_id = str(uuid4())

    new_ticket = Tickets.create(
        who=session["username"],
        issue=params["issue"],
        details=params["details"],
        uuid=ticket_id
    )
    new_ticket.save()

    ticket = Tickets.get(uuid=ticket_id)

    return True if ticket is not None else False


def list_tickets(packet):
    """
    Return tickets from the database depending on the method provided in the
    packet
    """

    params = packet["params"]
    rdb_conn = rethink.connect(host=app.config["RDB_HOST"],
                               port=app.config["RDB_PORT"],
                               db=app.config["RDB_DB"])

    if "sortBy" in params:
        if "who" in params["sortBy"]:
            if params["sortBy"]["who"] == "auth":
                params["sortBy"]["who"] = session["username"]

    if packet["method"] == "retrieve:search":
        search_term = params["string"].lower()

        results = rethink.table("tickets").filter(
            (lambda user:
             user["issue"].match("(?i){}".format(search_term))) |
            (lambda user:
             user["details"].match("(?i){}".format(search_term))) |
            (lambda user:
             user["representative"].match("(?i){}".format(search_term))) |
            (lambda user:
             user["who"].match("(?i){}".format(search_term)))
        ).limit(10).run(rdb_conn)

    elif packet["method"] == "retrieve:newest":
        Tickets()
        results = rethink.table("tickets").filter(
            {"resolved": False}).limit(10).run(rdb_conn)

    to_return = json.dumps([
        {
            "user": res["who"],
            "latest": res["issue"],
            "id": res["uuid"],
            "details": res["details"]
        } for res in results
    ])

    return to_return


def respond_to_ticket(packet):

    params = packet["params"]

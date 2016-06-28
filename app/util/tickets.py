"""
Provides ticket endpoints and controls for Cactus-CP
"""

import json
from functools import partial
import rethinkdb as rethink
import jrpc_helper as jrpc
from flask import jsonify, session
from flask_login import request, login_required
from werkzeug import ImmutableMultiDict
from ..models import Tickets, User, TicketResponse
from .. import app, csrf


@csrf.exempt
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
            "respond": partial(respond_to_ticket, data)
        }

        return_data = methods[data["method"]]()

        if return_data is not None:
            return_data = json.loads(return_data)

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

    params = packet.get("params", None)

    user = User.get(userName=session.get("username", None))

    new_ticket = Tickets.create(
        who=user,
        issue=params["issue"],
        details=params["details"],
    )
    new_ticket.save()

    ticket = Tickets.get(id=ticket_id)

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
             user["rep_id"].match("(?i){}".format(search_term))) |
            (lambda user:
             user["who"].match("(?i){}".format(search_term)))
        ).limit(10).run(rdb_conn)

    elif packet["method"] == "retrieve:newest":
        results = rethink.table("tickets").filter(
            {"resolved": False}).limit(10).run(rdb_conn)

    to_return = json.dumps([
        {
            "user": res["who"],
            "latest": res["issue"],
            "details": res["details"]
        } for res in results
    ])

    return to_return


def respond_to_ticket(packet):
    """
    Handles responses to support tickets
    """
    params = packet.get("params", None)

    if params is not None and all(key in params for key in [
        "response",
        "ticket_id",
        "user_id",
        "flags"
    ]):
        try:
            ticket_id = str(params.get("ticket_id", None))
            response = str(params.get("response", None))
            user_id = str(params.get("user_id", None))
            flags = int(params.get("flags", None))
        except ValueError as error:
            # Looks like we've got an incorrect type
            print(error)

        ticket = Tickets.get(id=ticket_id)
        user = User.get(id=user_id)

        if ticket is not None and user is not None:
            new_response = TicketResponse.create(
                who=user["id"],
                response=response,
                ticket=ticket["id"],
                flags=flags
            )
            new_response.save()

            to_return = TicketResponse.get(response=response,
                                           ticket=ticket["id"],
                                           who=user["id"])

            if to_return is not None:
                return json.dumps({
                    "flags": to_return["flags"],
                    "id": to_return["id"],
                    "ticket": to_return["ticket"],
                    "response": to_return["response"],
                    "who": to_return["who"]
                    })

        else:
            return None

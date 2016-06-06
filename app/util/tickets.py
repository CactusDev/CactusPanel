from flask import url_for, jsonify, render_template, session, Response
from flask.ext.login import request, login_required
from sqlalchemy import or_
from functools import partial
from ..models import Tickets
from uuid import uuid4
from .. import app, db, csrf_protect
from . import json_rpc
import json
import time


@csrf_protect.exempt
@login_required
@app.route("/support", methods=["POST"])
def support_router():
    if request.method == "POST":

        # NOTE: This doesn't actually see args sent by HTTPie, gotta figure out
        #       how to access those
        data = request.data.decode("utf-8")

        if data == "":
            error_packet = json_rpc.JSONRPCError(
                code=-32600,
                message="Invalid Request",
                data="No data was provided in POST request. POST must "
                        "include JSON-RPC compliant JSON data",
                response_id=None        # Required to be JSON-RPC compliant
            ).packet

            return jsonify(error_packet)

        data = json.loads(data)

        methods = {
            "retrieve:newest": partial(list_tickets, data),
            "retrieve:search": partial(list_tickets, data),
            "create": partial(create_ticket, data)
        }

        return_data = json.loads(methods[data["method"]]())

        response_packet = json_rpc.JSONRPCResult(
            response_id=data["id"] if "id" in data else None,
            result={"results": return_data},
        ).packet

        print(response_packet)

        return jsonify(response_packet)

    else:                          # Not GET/POST (somehow), method not allowed
        error_packet = json_rpc.JSONRPCError(
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

    params = packet["params"]

    ticket_id = str(uuid4())

    new_ticket = Tickets(
        who=session["username"],
        issue=params["issue"],
        details=params["details"],
        uuid=ticket_id
    )
    db.session.add(new_ticket)
    db.session.commit()

    ticket = Tickets.query.filter_by(uuid=ticket_id).first()

    if ticket is not None:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


def list_tickets(packet):

    params = packet["params"]

    if "sortBy" in params:
        if "who" in params["sortBy"]:
            if params["sortBy"]["who"] == "auth":
                params["sortBy"]["who"] = session["username"]

    if packet["method"] == "retrieve:search":
        search_term = params["string"].lower()

        results = Tickets.query.filter(or_(
            Tickets.issue.contains(search_term),
            Tickets.details.contains(search_term),
            Tickets.representative.contains(search_term),
            Tickets.who.contains(search_term)
        )).limit(10)
    elif packet["method"] == "retrieve:newest":
        results = db.session.query(Tickets).filter_by(
            resolved=False
        ).limit(10)

    to_return = json.dumps([
        {
            "user": res.who,
            "latest": res.issue,
            "id": res.uuid,
            "details": res.details
        } for res in results
    ])

    return to_return

from flask import url_for, jsonify, render_template, session, Response
from flask.ext.login import request, login_required
from sqlalchemy import or_
from ..models import Tickets
from uuid import uuid4
from .. import app, db
import json
import time


@login_required
@app.route("/support", methods=["GET", "POST"])
def support_router():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
    else:                          # Not GET/POST (somehow), method not allowed
        pass


@login_required
@app.route("/support/create", methods=["GET"])
def create_ticket_directive():
    if request.method == "GET":
        return render_template("directives/CreateSupportTicket.html")
    else:
        return "Method not allowed"


@login_required
@app.route("/support/respond", methods=["GET"])
def respond_ticket_directive():
    if request.method == "GET":
        return render_template("directives/RespondToTicket.html")
    else:
        return "Method not allowed"


def create_ticket():
    data = json.loads(request.data.decode("utf-8"))

    ticket_id = str(uuid4())

    new_ticket = Tickets(
        who=session["username"],
        issue=data["issue"],
        details=data["details"],
        uuid=ticket_id
    )
    db.session.add(new_ticket)
    db.session.commit()

    ticket = Tickets.query.filter_by(uuid=ticket_id).first()

    if ticket is not None:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


@login_required
@app.route("/support/list", methods=["GET", "POST"])
def ticket_list():
    if request.method == "POST":
        data = json.loads(request.data.decode("utf-8").lower())
        if "sortBy" in data:
            if "who" in data["sortBy"]:
                if data["sortBy"]["who"] == "auth":
                    data["sortBy"]["who"] = session["username"]

        search_term = data["search_string"]

        results = Tickets.query.filter(or_(
            Tickets.issue.contains(search_term),
            Tickets.details.contains(search_term),
            Tickets.representative.contains(search_term),
            Tickets.who.contains(search_term)
        )).limit(10)

        to_return = json.dumps([
            {
                "user": res.who,
                "latest": res.issue,
                "id": res.uuid,
                "details": res.details
             } for res in results
        ])

        return Response(to_return, mimetype="application/json")

    elif request.method == "GET":
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

        return Response(to_return, mimetype="application/json")

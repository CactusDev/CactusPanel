from flask import url_for, jsonify, render_template, session, Response
from flask.ext.login import request, login_required
from ..models import Tickets
from uuid import uuid4
from .. import app, db
import json
import time


@login_required
@app.route("/support/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "GET":
        return render_template("directives/CreateSupportTicket.html")
    elif request.method == "POST":
        data = json.loads(request.data.decode("utf-8"))

        ticket_id = str(uuid4())

        new_ticker = Tickets(
            who=session["username"],
            issue=data["issue"],
            details=data["details"],
            id=ticket_id
        )
        db.session.add(new_ticker)
        db.session.commit()

        ticket = Tickets.query.filter_by(id=ticket_id).first()

        if ticket is not None:
            print(ticket)

            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
    else:
        return "Method not supported."


@login_required
@app.route("/support/respond", methods=["GET", "POST"])
def ticket_response():
    if request.method == "GET":
        return render_template("directives/RespondToTicket.html")
    elif request.method == "POST":
        return "THINGS! #BlamePara"
    else:
        return "Method not supported."


@login_required
@app.route("/support/list", methods=["GET", "POST"])
def ticket_list():
    if request.method == "POST":
        data = json.loads(request.data.decode("utf-8"))
        # print(data)
        if "who" in data["sortBy"]:
            if data["sortBy"]["who"] == "auth":
                data["sortBy"]["who"] = session["username"]

        args = []
        if "searchTerm" in data:
            searchTerm = data["searchTerm"]
            print(searchTerm)
            args = [
                Tickets.details.contains(searchTerm),
                Tickets.issue.contains(searchTerm),
                Tickets.representative.contains(searchTerm),
                Tickets.who.contains(searchTerm)
            ]

        print(searchTerm)

        results = db.session.query(Tickets).filter(
            Tickets.details.contains(searchTerm),
            Tickets.issue.contains(searchTerm),
            Tickets.representative.contains(searchTerm),
            Tickets.who.contains(searchTerm)
        ).limit(10)

        for res in results:
            print(res)

        to_return = json.dumps([
            {"user": res.who, "latest": res.issue} for res in results
        ])

        print(to_return)

        return Response(to_return, mimetype="application/json")

    elif request.method == "GET":
        results = db.session.query(Tickets).filter_by(
                                                resolved=False,
                                                who=session["username"]
                                            ).limit(10)

        to_return = json.dumps([
            {"user": res.who, "latest": res.issue} for res in results
        ])

        print(to_return)
        return Response(to_return, mimetype="application/json")

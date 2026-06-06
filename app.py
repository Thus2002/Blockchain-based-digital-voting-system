from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from blockchain import Blockchain

from database import *

app = Flask(__name__)
app.secret_key = "voting_secret_key"

create_database()

blockchain = Blockchain()

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():

    name = request.form["name"]
    voter_id = request.form["voter_id"]
    email = request.form["email"]
    password = request.form["password"]

    status = register_voter(
        name,
        voter_id,
        email,
        password
    )

    if status:
        return "Registration Successful"

    return "Voter ID Already Exists"


@app.route("/login", methods=["POST"])
def login():

    voter_id = request.form["voter_id"]
    password = request.form["password"]

    voter = login_voter(
        voter_id,
        password
    )

    if voter:

        session["voter_id"] = voter_id

        return render_template(
            "vote.html",
            voter_id=voter_id
        )

    return "Invalid Login"


@app.route("/vote", methods=["POST"])
def vote():

    voter_id = session.get("voter_id")

    if not voter_id:
        return redirect("/")

    if has_voted(voter_id):
        return "You Have Already Voted"

    candidate = request.form["candidate"]

    record_vote(voter_id, candidate)

    blockchain.add_vote(
        {
            "voter_id": voter_id,
            "candidate": candidate
        }
    )

    return """
    <h2>Vote Submitted Successfully</h2>
    <a href='/results'>View Results</a>
    """


@app.route("/results")
def results():

    data = get_results()

    return render_template(
        "results.html",
        results=data
    )


@app.route("/admin")
def admin():

    return render_template(
        "admin_login.html"
    )


@app.route("/admin_login", methods=["POST"])
def admin_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == ADMIN_USER and password == ADMIN_PASS:

        voters = get_all_voters()

        return render_template(
            "admin_dashboard.html",
            voters=voters,
            chain=blockchain.chain
        )

    return "Invalid Admin Login"


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask

from storage.reader import read_tournament

app = Flask(__name__)


@app.route("/")
def frontpage():
    # TODO: This should work by reading the tournament from the db and then
    # passing to the front end. I think that this should just support GET
    # requests.
    return read_tournament()


@app.route("/team")
def show_team():
    # This is the get method for showing a team to a user.
    pass


@app.route("/team")
def update_team():
    # This is the post method for a user updating their team.
    pass

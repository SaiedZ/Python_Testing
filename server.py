import math

from flask import (Flask, render_template, request,
                   redirect, flash, url_for)

import config
from utils import (compare_str_date_to_now,
                   update_purchases_data,
                   verrify_condition_are_satisfied_to_purchase_places)
from data import data_utils

app = Flask(__name__)
app.secret_key = "something_special"
app.config.from_object("config")
app.jinja_env.filters["past_date"] = compare_str_date_to_now

competitions = data_utils.load_competitions()
clubs = data_utils.load_clubs()
purchases_dict = data_utils.load_purchases()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """
    Return the welcome template for known email or
    display an error message
    """
    try:
        return render_template(
            "welcome.html",
            club=[club for club in clubs if club["email"] ==
                  request.form["email"]][0],
            competitions=competitions)
    except IndexError:
        flash("Unknown email !", "error")
        return render_template("index.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        club = [c for c in clubs if c["name"] == club][0]
        competition = \
            [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club,
                               competitions=competitions)

    max_places_to_book = min(
        math.floor(int(club["points"]) / config.POINTS_PER_PLACE),
        int(competition["numberOfPlaces"]),
        config.MAX_BOOKABLE_PLACES,
    )
    return render_template(
        "booking.html",
        club=club,
        competition=competition,
        max_places_to_book=max_places_to_book,
    )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():

    competition = \
        [competition for competition in competitions if competition["name"] ==
         request.form["competition"]][0]
    competition_index = competitions.index(competition)

    club = [club for club in clubs if club["name"] == request.form["club"]][0]
    club_index = clubs.index(club)

    places_required = int(request.form["places"])
    places_already_bought = \
        data_utils.load_competition_places_purchased_by_club(club, competition)

    condition_satisfied = verrify_condition_are_satisfied_to_purchase_places(
        competition, club, places_required, places_already_bought, request)

    if not condition_satisfied:
        return render_template("booking.html", club=club,
                               competition=competition)

    club["points"] = \
        int(club["points"]) - (places_required * config.POINTS_PER_PLACE)
    competition["numberOfPlaces"] = \
        int(competition["numberOfPlaces"]) - places_required

    clubs[club_index] = club
    competitions[competition_index] = competition

    update_purchases_data(competition, club, places_required,
                          places_already_bought, purchases_dict,
                          clubs, competitions)

    flash("Great-booking complete!")

    return render_template("welcome.html", club=club,
                           competitions=competitions)


@app.route("/pointsBoard", methods=["GET"])
def pointsBoard():
    return render_template("points_board.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))

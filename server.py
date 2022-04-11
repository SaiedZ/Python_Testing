"""This module contains the views and some settings of the application"""

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

# loading data from json files
competitions = data_utils.load_competitions()
clubs = data_utils.load_clubs()
purchases_dict = data_utils.load_purchases()


@app.route("/")
def index():
    """Renders template index, homepage."""
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """Renders the welcome template for known email.
    If the email is not known, it displays an error message.
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
    """Render the booking template if the club's nam and
    competition's name in the url exist.
    Otherwise, il will display the welcome template with
    an error message.
    """
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
    """Manage the purchasing od places by clubs.
    
    If conditions are satisfied, the club can purchase
    the required number of places. Then, the welcome template
    will be displayer with a success message.
    
    If conditions are not satisfied, the booking template will
    be displayed with a failure message.
    """
    # get the competition from competitions and its index
    competition = \
        [competition for competition in competitions if competition["name"] ==
         request.form["competition"]][0]
    competition_index = competitions.index(competition)

    # get the club from clubs and its index
    club = [club for club in clubs if club["name"] == request.form["club"]][0]
    club_index = clubs.index(club)

    places_required = int(request.form["places"])
    places_already_bought = \
        data_utils.load_competition_places_purchased_by_club(club, competition)

    # verrify if conditions to buy places are satisfied
    condition_satisfied = verrify_condition_are_satisfied_to_purchase_places(
        competition, club, places_required, places_already_bought, request)

    if not condition_satisfied:
        return render_template("booking.html", club=club,
                               competition=competition)

    # updating club's points, competition's places and bought places
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


@app.route("/points_board", methods=["GET"])
def points_board():
    """Render the template for displaying the points board."""
    return render_template("points_board.html", clubs=clubs)


@app.route("/logout")
def logout():
    """Logout the club by rendering the index page."""
    return redirect(url_for("index"))

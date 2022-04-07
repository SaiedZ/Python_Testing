import math

from flask import Flask, render_template, request, redirect, flash, url_for

import config
from utils import compare_str_date_to_now
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
    if [club for club in clubs if club["email"] == request.form["email"]]:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash("Unknown email !", "error")
        return render_template("index.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)

    max_places_to_book = min(
        math.floor(int(foundClub["points"]) / config.POINTS_PER_PLACE),
        int(foundCompetition["numberOfPlaces"]),
        config.MAX_BOOKABLE_PLACES,
    )
    return render_template(
        "booking.html",
        club=foundClub,
        competition=foundCompetition,
        max_places_to_book=max_places_to_book,
    )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():

    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    club_index = clubs.index(club)
    competition_index = competitions.index(competition)
    places_required = int(request.form["places"])
    places_already_bought = data_utils.load_competition_places_purchased_by_club(club, competition)

    problem_to_purchase = False

    if compare_str_date_to_now(competition["date"]):
        flash("You can't book a place on a post-dated competition! ")
        problem_to_purchase = True

    if int(request.form["places"]) <= 0:
        flash("Places to book should be an integer > 0")
        problem_to_purchase = True

    if places_already_bought >= config.MAX_BOOKABLE_PLACES:
        flash("You already booked the maximum of places for this competition! ")
        problem_to_purchase = True

    max_places_to_book = math.floor(int(club["points"]) / config.POINTS_PER_PLACE)

    if places_required > max_places_to_book:
        flash("You don't have enough points ! ")
        problem_to_purchase = True

    if places_required > int(competition["numberOfPlaces"]):
        flash("You can't book more places than available ! ")
        problem_to_purchase = True

    if (places_required + places_already_bought) > config.MAX_BOOKABLE_PLACES:
        flash(
            f"You are not allowed to purchase more than {config.MAX_BOOKABLE_PLACES} places ! "
        )
        flash(f"You already bougth {places_already_bought} for this competition! ")
        problem_to_purchase = True

    if problem_to_purchase:
        return render_template("booking.html", club=club, competition=competition)

    club["points"] = int(club["points"]) - (places_required * config.POINTS_PER_PLACE)
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required

    clubs[club_index] = club
    competitions[competition_index] = competition
    data_utils.update_purchases(
        purchases_dict,
        club["email"],
        competition["name"],
        places_already_bought + places_required,
    )
    data_utils.update_json_data("data/clubs.json", {"clubs": clubs})
    data_utils.update_json_data("data/competitions.json", {"competitions": competitions})
    data_utils.update_json_data("data/purchases.json", purchases_dict)

    flash("Great-booking complete!")

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/pointsBoard", methods=["GET"])
def pointsBoard():
    return render_template("points_board.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))

"""This module contains utility functions."""

from flask import flash

from datetime import datetime
import math

import config
from data import data_utils


def compare_str_date_to_now(str_date):
    """Return True if the date passed inf the params is
    a past date, otherwise it return False."""
    datetime_object = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    return datetime_object < datetime.now()


def update_purchases_data(competition, club, places_required,
                          places_already_bought, purchases_dict,
                          clubs, competitions):
    """Updates the purchases and the json files of purchases and
    clubs and competitions.
    """
    data_utils.update_purchases(
        purchases_dict,
        club["email"],
        competition["name"],
        places_already_bought + places_required,
    )
    data_utils.update_json_data("data/clubs.json",
                                {"clubs": clubs})
    data_utils.update_json_data("data/competitions.json",
                                {"competitions": competitions})
    data_utils.update_json_data("data/purchases.json",
                                purchases_dict)


def verrify_condition_are_satisfied_to_purchase_places(
    competition, club, places_required, places_already_bought, request
):
    """
    Verrify if all conditions are satisfied to allow a club to purchase
    places.
    
    If some condition are not satisfied, a message is flashed
    and a booleen value is returned as False.
    
    If all conditions are satisfied True is returned.
    """
    problem_to_purchase = True
    # can't book postdated competition
    if compare_str_date_to_now(competition["date"]):
        flash("You can't book a place on a post-dated competition! ")
        problem_to_purchase = False
    # négati places numbers are not accepted
    if int(request.form["places"]) <= 0:
        flash("Places to book should be an integer > 0")
        problem_to_purchase = False
    # can't book if already booked the maximum allowed number
    if places_already_bought >= config.MAX_BOOKABLE_PLACES:
        flash(
            "You already booked the maximum of places for this competition! ")
        problem_to_purchase = False

    max_places_to_book = \
        math.floor(int(club["points"]) / config.POINTS_PER_PLACE)
    # can't book more than the maximum allowed
    if places_required > max_places_to_book:
        flash("You don't have enough points ! ")
        problem_to_purchase = False
    # can't book more than available places
    if places_required > int(competition["numberOfPlaces"]):
        flash("You can't book more places than available ! ")
        problem_to_purchase = False
    # can't book if the sum of already booked places and places to book is > max
    if (places_required + places_already_bought) > config.MAX_BOOKABLE_PLACES:
        flash(
            f"You are not allowed to purchase more than {config.MAX_BOOKABLE_PLACES} places ! "
        )
        flash(
            f"You already bougth {places_already_bought} for this competition! ")
        problem_to_purchase = False

    return problem_to_purchase

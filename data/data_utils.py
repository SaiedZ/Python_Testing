"""This module contains utils for managing json data."""

import json


def load_clubs():
    """Returns the list of clubs from the json file."""
    with open("data/clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    """Returns the list of competitions from the json file."""
    with open("data/competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def load_purchases():
    """Returns a dict of purchases from the json file."""
    with open("data/purchases.json") as purchases_file:
        purchases_dict = json.load(purchases_file)
        return purchases_dict


def load_competition_places_purchased_by_club(club, competition):
    """Return the number of purchaed places by a club for a given competition."""
    club_email = club["email"]
    competition_name = competition["name"]
    purchases_dict = load_purchases()
    try:
        purchased_places = int(purchases_dict[club_email][competition_name])
    except KeyError:
        purchased_places = 0

    return purchased_places


def update_json_data(file, data):
    """Updates a json files."""
    with open(file, "w") as file:
        json.dump(data, file, indent=4, separators=(",", ": "))


def update_purchases(purchases_dict, club_email, competition_name, value):
    """
    Updates purchases to avoid keyerrors when a club buy places
    for a competition for the first time.
    """
    if club_email in purchases_dict and competition_name in purchases_dict:
        purchases_dict[club_email][competition_name] = value
    else:
        purchases_dict[club_email] = {competition_name: value}

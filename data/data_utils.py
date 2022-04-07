import json


def load_clubs():
    with open("data/clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    with open("data/competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def load_purchases():
    with open("data/purchases.json") as purchases_file:
        purchases_dict = json.load(purchases_file)
        return purchases_dict


def load_competition_places_purchased_by_club(club, competition):
    club_email = club["email"]
    competition_name = competition["name"]
    purchases_dict = load_purchases()
    try:
        purchased_places = int(purchases_dict[club_email][competition_name])
    except KeyError:
        purchased_places = 0

    return purchased_places


def update_json_data(file, data):
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

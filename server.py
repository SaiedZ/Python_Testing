import json, math
from datetime import datetime

import config
from flask import Flask,render_template,request,redirect,flash,url_for


app = Flask(__name__)
app.secret_key = 'something_special'
app.config.from_object('config')


def compare_str_date_to_now(str_date):
    datetime_object = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
    return datetime_object < datetime.now()


app.jinja_env.filters['past_date'] = compare_str_date_to_now


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions



competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    if [club for club in clubs if club['email'] == request.form['email']]:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    else:
        flash("Unknown email !", "error")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition:
        max_places_to_book = min(
            math.floor(int(foundClub['points']) / config.POINTS_PER_PLACE),
            int(foundCompetition['numberOfPlaces']),
            config.MAX_BOOKABLE_PLACES,
        )
        return render_template('booking.html',club=foundClub,competition=foundCompetition,max_places_to_book=max_places_to_book)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > config.MAX_BOOKABLE_PLACES:
        flash(f"You are not allowed to purchase more than {config.MAX_BOOKABLE_PLACES} places ! ")
        return render_template('booking.html', club=club, competition=competition)

    max_places_to_book = math.floor(int(club['points']) / config.POINTS_PER_PLACE)

    if placesRequired > max_places_to_book:
        flash("You don't have enough points ! ")
        return render_template('booking.html', club=club, competition=competition)

    if placesRequired > int(competition['numberOfPlaces']):
        flash("You can't book more places than available ! ")
        return render_template('booking.html', club=club, competition=competition)

    club['points'] = int(club['points']) - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired

    flash('Great-booking complete!')

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

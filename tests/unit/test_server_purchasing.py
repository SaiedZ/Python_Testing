import pytest

import server
from tests.conftest import client


class TestPurchasing:

    def setup_method(self, method):
        self.app = server.app
        self.mocked_clubs = [
            {"name": "Simp Ly", "email": "john@simplylift.co", "points": "13"},
        ]
        self.mocked_competitions = [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
        self.app_context = self.app.test_request_context()
        self.app_context.push()  # push it

    def tearDown(self):
        self.context.pop()  # pop it

    def test_purshasing_should_reduce_places_and_club_points(self, client, mocker):
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)

        club, competition = self.mocked_clubs[0], self.mocked_competitions[0]
        places_to_book = 10
        expected_remaining_places = int(competition['numberOfPlaces']) - places_to_book
        expected_remaining_points = int(club['points']) - places_to_book

        response = client.post('/purchasePlaces', data={'competition': competition["name"], 'club': club["name"], 'places': places_to_book})

        data = response.data.decode()

        assert response.status_code == 200
        assert data.find("Great-booking complete!") != -1
        assert competition['numberOfPlaces'] == expected_remaining_places
        assert club['points'] == expected_remaining_points

from flask import url_for
import pytest

import server
from server import book
from tests.conftest import client


class TestBooking:

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
        self.wrong_club_name = "Does Not Exist"
        self.app_context = self.app.test_request_context()
        self.app_context.push()  # push it

    def tearDown(self):
        self.context.pop()  # pop it

    def test_book_view_should_return_booking_template_if_club_competition(
        self, client, mocker
    ):
        """
        Testing if by using an existing club and competition the app will show
        the content of the booking.html template
        """
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)

        club, competition = self.mocked_clubs[0], self.mocked_competitions[0]
        response = client.get(
            url_for(
                "book",
                competition=competition["name"],
                club=club["name"],
                _external=False,
            )
        )

        data = response.data.decode()

        assert response.status_code == 200
        assert response.request.url == url_for(
            "book", competition=competition["name"], club=club["name"], _external=True
        )
        assert data.find("Places available:") != -1

    def test_book_view_should_return_error_if_not_club_or_competition(
        self, client, mocker
    ):
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)

        competition = self.mocked_competitions[0]
        response = client.get(
            url_for(
                "book",
                competition=competition["name"],
                club=self.wrong_club_name,
                _external=False,
            )
        )

        data = response.data.decode()

        assert response.status_code == 200
        assert response.request.url == url_for(
            "book", competition=competition["name"], club=self.wrong_club_name, _external=True
        )
        assert data.find("Something went wrong-please try again") != -1
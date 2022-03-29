import pytest

import server
from tests.conftest import client


class TestLogin:

    def setup_method(self, method):
        self.wrong_email = "admin@irontemple.com"
        self.moked_clubs = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        ]

    def test_login_works_with_correct_email(self, client, mocker):

        mocker.patch.object(server, 'clubs', self.moked_clubs)

        club = self.moked_clubs[0]
        response = client.post("/showSummary", data={'email': club['email']})
        data = response.data.decode()

        assert response.status_code == 200
        assert response.request.path == "/showSummary"
        assert data.find("Welcome") != -1

    def test_login_not_possible_with_wrong_email(self, client, mocker):

        mocker.patch.object(server, 'clubs', self.moked_clubs)

        response = client.post("/showSummary", data={'email': self.wrong_email})
        data = response.data.decode()

        assert response.status_code == 200
        assert response.request.path == "/showSummary"
        assert data.find("<p>Unknown email !</p>") != -1

import pytest

import server
from tests.conftest import client


class TestPointsBoard:
    def setup_method(self, method):
        self.app = server.app
        self.mocked_clubs = [
            {"name": "Simp Ly", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Te", "email": "admin@iron.com", "points": "4"},
        ]

    def test_should_access_home(self, client):
        assert client.get("/").status_code == 200

    def test_board_correctly_displays_clubs(self, client, mocker):
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        response = client.get("/pointsBoard")
        assert response.status_code == 200
        data = response.data.decode()
        for club in self.mocked_clubs:
            assert club["name"] in data
            assert str(club["points"]) in data

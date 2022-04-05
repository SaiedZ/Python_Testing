import pytest

import server, config
from tests.conftest import client


class TestPurchasing:
    def setup_method(self, method):
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
                "date": "2026-10-22 13:30:00",
                "numberOfPlaces": "12",
            },
        ]

    def test_purshasing_should_reduce_places_and_club_points(self, client, mocker):
        """
        Testing if after purshasing places, the number of places and club's
        points are reduced
        """
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)
        mocker.patch.object(config, "MAX_BOOKABLE_PLACES", 100)
        mocker.patch.object(config, "POINTS_PER_PLACE", 1)
        mocker.patch("server.update_purchases", return_value=None)
        mocker.patch("server.update_json_data", return_value=None)

        club, competition = self.mocked_clubs[0], self.mocked_competitions[1]
        places_to_book = 2
        expected_remaining_places = int(competition["numberOfPlaces"]) - places_to_book
        expected_remaining_points = int(club["points"]) - places_to_book

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": places_to_book,
            },
        )

        data = response.data.decode()

        assert response.status_code == 200
        assert data.find("Great-booking complete!") != -1
        assert competition["numberOfPlaces"] == expected_remaining_places
        assert club["points"] == expected_remaining_points

    def test_purshasing_should_not_work_if_not_enough_points_or_places(
        self, client, mocker
    ):
        """
        Testing if purshasing doesn't work if not enough points or places
        """
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)
        mocker.patch.object(config, "MAX_BOOKABLE_PLACES", 100)
        mocker.patch.object(config, "POINTS_PER_PLACE", 1)

        club, competition = self.mocked_clubs[0], self.mocked_competitions[1]
        places_to_book_more_than_points = 20
        places_to_book_more_than_places = 13

        response_not_enough_points = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": places_to_book_more_than_points,
            },
        )
        data_not_enough_points = response_not_enough_points.data.decode()

        response_not_enough_places = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": places_to_book_more_than_places,
            },
        )
        data_not_enough_places = response_not_enough_places.data.decode()

        assert data_not_enough_points.find("You don&#39;t have enough points ! ") != -1
        assert (
            data_not_enough_places.find(
                "You can&#39;t book more places than available ! "
            )
            != -1
        )

    def test_club_can_not_book_more_places_than_allowed(self, client, mocker):
        """
        Testing if purshasing doesn't work if a club want to book
        more than the allowed number of places per club
        """
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)

        club, competition = self.mocked_clubs[0], self.mocked_competitions[1]

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": config.MAX_BOOKABLE_PLACES * 2,
            },
        )

        data = response.data.decode()

        assert (
            data.find(
                f"You are not allowed to purchase more than {config.MAX_BOOKABLE_PLACES} places ! "
            )
            != -1
        )

    def test_club_can_not_book_postdated_competition(self, client, mocker):
        """
        Testing the purchasin view to verrify that a club
        can't book a postdated competition
        """
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)

        club, competition = self.mocked_clubs[0], self.mocked_competitions[0]

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": 1,
            },
        )

        data = response.data.decode()

        assert (
            data.find("You can&#39;t book a place on a post-dated competition! ") != -1
        )

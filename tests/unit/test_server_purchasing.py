"""This module contains unit tests for purchasing."""

import server
import config


class TestPurchasing:

    def test_purshasing_should_reduce_places_and_club_points(
        self, client, mocker, mocked_clubs, mocked_competitions,
        test_club, not_postdated_competition
    ):
        """
        Testing if after purshasing places, the number of places and club's
        points are reduced
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)
        mocker.patch.object(config, "MAX_BOOKABLE_PLACES", 100)
        mocker.patch.object(config, "POINTS_PER_PLACE", 1)
        mocker.patch("data.data_utils.update_purchases", return_value=None)
        mocker.patch("data.data_utils.update_json_data", return_value=None)

        places_to_book = 2
        expected_remaining_places = \
            int(not_postdated_competition["numberOfPlaces"]) - places_to_book
        expected_remaining_points = int(test_club["points"]) - places_to_book

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": not_postdated_competition["name"],
                "club": test_club["name"],
                "places": places_to_book,
            },
        )

        data = response.data.decode()

        assert response.status_code == 200
        assert data.find("Great-booking complete!") != -1
        assert not_postdated_competition["numberOfPlaces"] == \
            expected_remaining_places
        assert test_club["points"] == expected_remaining_points

    def test_purshasing_should_not_work_if_not_enough_points_or_places(
        self, client, mocker, mocked_clubs, mocked_competitions,
        test_club, not_postdated_competition, places_to_book_more_than_points,
        places_to_book_more_than_places
    ):
        """
        Testing if purshasing doesn't work if not enough points or places
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)
        mocker.patch.object(config, "MAX_BOOKABLE_PLACES", 100)
        mocker.patch.object(config, "POINTS_PER_PLACE", 1)

        response_not_enough_points = client.post(
            "/purchasePlaces",
            data={
                "competition": not_postdated_competition["name"],
                "club": test_club["name"],
                "places": places_to_book_more_than_points,
            },
        )
        data_not_enough_points = response_not_enough_points.data.decode()

        response_not_enough_places = client.post(
            "/purchasePlaces",
            data={
                "competition": not_postdated_competition["name"],
                "club": test_club["name"],
                "places": places_to_book_more_than_places,
            },
        )
        data_not_enough_places = response_not_enough_places.data.decode()

        assert data_not_enough_points.find(
            "You don&#39;t have enough points ! ") != -1
        assert (
            data_not_enough_places.find(
                "You can&#39;t book more places than available ! "
            )
            != -1
        )

    def test_club_can_not_book_more_places_than_allowed(
        self, client, mocker, mocked_clubs, mocked_competitions,
        test_club, not_postdated_competition
    ):
        """
        Testing if purshasing doesn't work if a club want to book
        more than the allowed number of places per club
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": not_postdated_competition["name"],
                "club": test_club["name"],
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

    def test_club_can_not_book_postdated_competition(
        self, client, mocker, mocked_clubs, mocked_competitions,
        test_club, post_dated_competition
    ):
        """
        Testing the purchasin view to verrify that a club
        can't book a postdated competition
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": post_dated_competition["name"],
                "club": test_club["name"],
                "places": 1,
            },
        )

        data = response.data.decode()

        assert (
            data.find(
                "You can&#39;t book a place on a post-dated competition! "
                ) != -1
        )

    def test_purshasing_should_not_work_if_negatif_number_places(
        self, client, mocker, mocked_clubs, mocked_competitions,
        test_club, not_postdated_competition,
    ):
        """
        Testing if purshasing doesn't work if the number of places is negatif.
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": not_postdated_competition["name"],
                "club": test_club["name"],
                "places": -1,
            },
        )
        data = response.data.decode()

        assert (
            data.find(
                "Places to book should be an integer &gt; 0"
            )
            != -1
        )
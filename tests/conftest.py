import pytest

import server


@pytest.fixture
def client():
    server.app.config.update({"TESTING": True})
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def mocked_clubs():
    return [
                {"name": "Simp Ly",
                 "email": "john@simplylift.co",
                 "points": "13"},
            ]


@pytest.fixture
def mocked_competitions():
    return [
                {
                    "name": "Spring Festival",
                    "date": "2020-03-27 10:00:00",
                    "numberOfPlaces": "25",
                },
                {
                    "name": "Fall Classic",
                    "date": "2026-10-22 13:30:00",
                    "numberOfPlaces": "13",
                },
            ]


@pytest.fixture
def wrong_club():
    return {"name": "wrong",
            "email": "wrong@wrong.wrong",
            "points": "13"}


@pytest.fixture
def test_club(mocked_clubs):
    return mocked_clubs[0]


@pytest.fixture
def not_postdated_competition(mocked_competitions):
    return mocked_competitions[1]


@pytest.fixture
def places_to_book_more_than_points(test_club):
    return int(test_club["points"]) * 20


@pytest.fixture
def post_dated_competition(mocked_competitions):
    return mocked_competitions[0]


@pytest.fixture
def places_to_book_more_than_places(not_postdated_competition):
    return int(not_postdated_competition["numberOfPlaces"]) * 20

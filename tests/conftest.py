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
                {"name": "Simp Ly", "email": "john@simplylift.co", "points": "13"},
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
    return mocked_clubs, mocked_competitions

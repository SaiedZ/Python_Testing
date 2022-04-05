import server
import config


class TestIntegrationClass:
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
                "date": "2026-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
        self.app_context = self.app.test_request_context()
        self.app_context.push()  # push it

    def tearDown(self):
        self.context.pop()  # pop it

    def test_registred_club_should_access_home_and_login_logout(self, client):
        """
        Tests club can login then visit the home page then logout
        """
        club = self.mocked_clubs[0]

        # index
        assert client.get("/").status_code == 200

        # Login
        data = {"email": club["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

        # Logout
        logout_page = client.get("/logout")
        assert logout_page.status_code == 302

    def test_registred_club_can_book_places_after_login(self, client, mocker):
        """
        Tests club can login then book places
        """

        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)
        mocker.patch("server.update_purchases", return_value=None)
        mocker.patch("server.update_json_data", return_value=None)

        club = self.mocked_clubs[0]
        competition = self.mocked_competitions[1]

        # Login
        data = {"email": club["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

        # Reach booking page
        booking_page = client.get(f'/book/{competition["name"]}/{club["name"]}')
        assert booking_page.status_code == 200

        # Book 2 places
        places = 2
        points_to_book = places * config.POINTS_PER_PLACE
        initial_club_points = int(club["points"])
        data = {
            "club": club["name"],
            "competition": competition["name"],
            "places": places,
        }
        reservation = client.post("/purchasePlaces", data=data)
        remaining_club_points = initial_club_points - points_to_book
        assert reservation.status_code == 200
        remaining_club_points = initial_club_points - places * config.POINTS_PER_PLACE
        assert f"Points available: {remaining_club_points}" in reservation.data.decode(
            "utf-8"
        )

import server
import config


class TestIntegrationClass:

    def setup_method(self, method):
        self.app = server.app
        self.app_context = self.app.test_request_context()
        self.app_context.push()  # push it

    def tearDown(self):
        self.context.pop()  # pop it

    def test_registred_club_should_access_home_and_login_logout(
        self, client, mocked_clubs
    ):
        """
        Tests club can login then visit the home page then logout
        """
        club = mocked_clubs[0]

        # index page
        assert client.get("/").status_code == 200

        # Test the login
        data = {"email": club["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

        # Test the logout
        logout_page = client.get("/logout")
        assert logout_page.status_code == 302

    def test_registred_club_can_book_places_after_login(
        self, client, mocked_clubs, mocked_competitions, mocker
    ):
        """
        Tests club can login then book places
        """

        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)
        mocker.patch("data.data_utils.update_purchases", return_value=None)
        mocker.patch("data.data_utils.update_json_data", return_value=None)

        club = mocked_clubs[0]
        competition = mocked_competitions[1]

        # Login a user
        data = {"email": club["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

        # Visiting the booking,page
        booking_page = client.get(
            f'/book/{competition["name"]}/{club["name"]}')
        assert booking_page.status_code == 200

        # purchasing 3 places
        places = 3
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
        remaining_club_points = \
            initial_club_points - places * config.POINTS_PER_PLACE
        assert f"Points available: {remaining_club_points}"\
            in reservation.data.decode("utf-8")

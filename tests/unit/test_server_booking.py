from flask import url_for

import server


class TestBooking:

    def setup_method(self, method):
        """
        This is used to be able to use the url_for.
        """
        self.app = server.app
        self.app_context = self.app.test_request_context()
        self.app_context.push()  # push it

    def tearDown(self):
        """
        Pop the test_request_context() that was added in the
        setup_method
        """
        self.context.pop()  # pop it

    def test_book_view_should_return_booking_template_if_club_competition(
        self, client, mocker, mocked_clubs, mocked_competitions,
        test_club, not_postdated_competition
    ):
        """
        Testing if by using an existing club and competition the app will show
        the content of the booking.html template
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)

        url_to_test = url_for(
            "book",
            competition=not_postdated_competition["name"],
            club=test_club["name"],
            _external=True,
        )
        response = client.get(url_to_test)
        data = response.data.decode()

        assert response.status_code == 200
        assert response.request.url == url_to_test
        assert data.find("Places available:") != -1

    def test_book_view_should_return_error_if_not_club_or_competition(
        self, client, mocker, mocked_clubs, wrong_club,
        mocked_competitions, not_postdated_competition
    ):
        """
        Testing if by using a wrong club the app will show
        an error message
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)

        url_to_test = url_for(
            "book",
            competition=not_postdated_competition["name"],
            club=wrong_club['name'],
            _external=True,
        )
        response = client.get(url_to_test)
        data = response.data.decode()

        assert response.status_code == 200
        assert response.request.url == url_to_test
        assert data.find("Something went wrong-please try again") != -1

    def test_club_can_only_book_future_competition(
        self, client, mocker, mocked_clubs,
        test_club, mocked_competitions
    ):
        """
        Testing the welcome template
        with one post dated competition and one valid we shoul have
        only one link with "book places"
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        mocker.patch.object(server, "competitions", mocked_competitions)

        response = client.post(
            "/showSummary", data={"email": test_club["email"]}
        )
        list_response_text = list(str(response.data).split(" "))
        occurence_book_response = list_response_text.count("Book")
        assert response.status_code == 200
        assert occurence_book_response == 1

import pytest

import server
from tests.conftest import client


class TestLogin:
    def setup_method(self, method):
        self.wrong_email = "admin@irontemple.com"
        self.moked_clubs = [
            {"name": "Simp Ly", "email": "john@simplylift.co", "points": "13"},
        ]

    def test_login_works_with_correct_email(self, client, mocker):
        """
        Testing if by entering a existing email the app will show
        the content of the welcome.html template
        """
        mocker.patch.object(server, "clubs", self.moked_clubs)

        club = self.moked_clubs[0]
        response = client.post("/showSummary", data={"email": club["email"]})

        self._test_root_response_code_template(response, "/showSummary", "Welcome")

    def test_login_not_possible_with_wrong_email(self, client, mocker):
        """
        Testing if by entering a wrond email the app will not crash,
        instead, it should show an error message : 'Unknown email !'
        """
        mocker.patch.object(server, "clubs", self.moked_clubs)

        response = client.post("/showSummary", data={"email": self.wrong_email})

        self._test_root_response_code_template(
            response, "/showSummary", "<p>Unknown email !</p>"
        )

    def _test_root_response_code_template(self, response, root, html_tag):
        data = response.data.decode()
        assert response.status_code == 200
        assert response.request.path == root
        assert data.find(html_tag) != -1

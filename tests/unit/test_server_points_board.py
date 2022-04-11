import server


class Testpoints_board:

    def test_should_access_home(self, client):
        """
        Test the response code for the home page.
        """
        assert client.get("/").status_code == 200

    def test_board_correctly_displays_clubs(
        self, client, mocker, mocked_clubs
    ):
        """
        Test the reponse for the /points_board page and
        that club and theire points are displayed.
        """
        mocker.patch.object(server, "clubs", mocked_clubs)
        response = client.get("/points_board")
        assert response.status_code == 200
        data = response.data.decode()
        for club in mocked_clubs:
            assert club["name"] in data
            assert str(club["points"]) in data

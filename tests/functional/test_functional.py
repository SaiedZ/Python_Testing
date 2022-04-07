from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

from server import load_clubs, load_competitions, load_purchases
from server import update_json_data

clubs = load_clubs()
competitions = load_competitions()
purchases = load_purchases()


class TestLogingsPurchasingPlaces:

    """
    Functional tests to ensure that:
    1. login with bad email doesn't work
    2. registred club can login, purchase places and
    logout successfully
    """

    def setup_method(self, method):
        """
        Setup selenium web driver using Firefox as a browser
        """
        self.browser = webdriver.Firefox(
            service=Service("tests/functional/geckodriver")
        )

    def teardown_method(self, method):
        """
        Selenium web driver is closed
        data are recoverd to the initial state by updating
        the json files: clubs, competitions, purchases
        """
        self.browser.close()
        update_json_data("clubs.json", {"clubs": clubs})
        update_json_data("competitions.json", {"competitions": competitions})
        update_json_data("purchases.json", purchases)

    def test_login_with_wrong_email(self):
        """
        Test that it's not possible to login with a wrong email
        1) A GET request is sent to 'http://127.0.0.1:5000/' page
        2) A POST request is sent to '/showSummary' page with a
        wrong email: The response includes "Unknown email !"
        """
        self.browser.get("http://127.0.0.1:5000/")
        self._find_field_send_key_click("email", "wrong@wrong.com")
        assert self.browser.current_url == "http://127.0.0.1:5000/showSummary"
        element_p = self.browser.find_element(by=By.TAG_NAME, value="p").text
        assert element_p == "Unknown email !"

    def test_login_and_purchasing_places_then_logout(self):
        """
        Test that registred club can login, purchase places and
        logout successfully
        """
        # login user with registred email
        club = clubs[0]
        self.browser.get("http://127.0.0.1:5000/")
        element = self.browser.find_element(by=By.TAG_NAME, value="h1").text
        assert element == "Welcome to the GUDLFT Registration Portal!"
        self._find_field_send_key_click("email", club["email"])
        assert self.browser.current_url == "http://127.0.0.1:5000/showSummary"
        element_h3 = self.browser.find_element(by=By.TAG_NAME, value="h3").text
        assert element_h3 == "Competitions:"

        # connected user chooses a competition and click on book link
        book_link = self.browser.find_element(
            by=By.XPATH, value="//ul/li[2]/a"
        )
        book_link.click()
        assert (
            self.browser.current_url
            == "http://127.0.0.1:5000/book/Fall%20Classic/Simply%20Lift"
        )

        # connected user purchases places
        self._find_field_send_key_click("places", 1)
        remaining_places = self.browser.find_element(
            by=By.XPATH, value="//ul/li[2]"
        ).text
        expected_number_places = str(int(competitions[1]["numberOfPlaces"])-1)
        assert expected_number_places in remaining_places
        element_li = self.browser.find_element(by=By.TAG_NAME, value="li").text
        assert element_li == "Great-booking complete!"

        # logout
        logout_link = self.browser.find_element(by=By.XPATH, value="//body/a")
        logout_link.click()
        assert self.browser.current_url == "http://127.0.0.1:5000/"

    def _find_field_send_key_click(self, field, input_value):
        field = self.browser.find_element(by=By.NAME, value=field)
        field.send_keys(input_value)
        enter_button = self.browser.find_element(
            by=By.TAG_NAME, value="button"
        )
        enter_button.click()

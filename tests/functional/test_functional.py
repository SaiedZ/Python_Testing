from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

from math import floor
import pytest
import server, config
from server import loadClubs, loadCompetitions, update_json_data, load_purchases

from selenium import webdriver


clubs = loadClubs()
competitions = loadCompetitions()
purchases = load_purchases()


class TestBookingPlaces:

    def setup_method(self, method):
        self.browser = webdriver.Firefox(service=Service('tests/functional/geckodriver'))
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

    def teardown_method(self, method):
        self.browser.close()
        update_json_data("clubs.json", {"clubs": clubs})
        update_json_data("competitions.json", {"competitions": competitions})
        update_json_data("purchases.json", purchases)

    def test_signup_with_bad_email(self):

        self.browser.get('http://127.0.0.1:5000/')
        email = self.browser.find_element(by=By.NAME, value='email')
        email.send_keys('wrong@wrong.com')
        enter = self.browser.find_element(by=By.TAG_NAME, value='button')
        enter.click()
        assert self.browser.current_url == "http://127.0.0.1:5000/showSummary"
        element_h1 = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        assert element_h1 == "Welcome to the GUDLFT Registration Portal!"

    def test_signup_and_booking_places_and_logout(self, mocker):
        mocker.patch.object(server, "clubs", self.mocked_clubs)
        mocker.patch.object(server, "competitions", self.mocked_competitions)
        # login user
        club = self.mocked_clubs[0]
        self.browser.get("http://127.0.0.1:5000/")
        element = self.browser.find_element(by=By.TAG_NAME, value="h1").text
        assert element == "Welcome to the GUDLFT Registration Portal!"
        email = self.browser.find_element(by=By.NAME, value="email")
        email.send_keys(club["email"])
        enter = self.browser.find_element(by=By.TAG_NAME, value='button')
        enter.click()
        assert self.browser.current_url == "http://127.0.0.1:5000/showSummary"
        element_h3 = self.browser.find_element(by=By.TAG_NAME, value='h3').text
        assert element_h3 == "Competitions:"
    '''
        # user chooses a competition and click on book in order to purchase places
        book_link = self.browser.find_element(by=By.XPATH, value='//ul/li[2]/a')
        book_link.click()
        assert self.browser.current_url == "http://127.0.0.1:5000/book/Fall%20Classic/Simply%20Lift"

        # user books places
        number_of_places = self.browser.find_element(by=By.NAME, value='places')
        number_of_places.send_keys('4')
        valid_booking = self.browser.find_element(by=By.TAG_NAME, value='button')
        valid_booking.click()
        display_number_of_places = self.browser.find_element(by=By.XPATH, value='//ul/li[2]').text
        assert '9' in display_number_of_places

        # logout user
        logout = self.browser.find_element(by=By.XPATH, value='//body/a')
        logout.click()
        assert self.browser.current_url == "http://127.0.0.1:5000/"
      
    '''
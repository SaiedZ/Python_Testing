from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

from flask import Flask
from flask_testing import LiveServerTestCase

from math import floor

from server import loadClubs, loadCompetitions, app
from server import load_purchases, update_purchases, load_purchases

from random import choice, randrange
from selenium import webdriver


clubs = loadClubs()
competitions = loadCompetitions()
purchases = load_purchases()


class TestBookingPlaces(LiveServerTestCase):

    def create_app(self):
        # app = Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_signup_with_bad_email(self):

        self.browser = webdriver.Firefox(service=Service('tests/functional/geckodriver'))
        self.browser.get('http://127.0.0.1:5000/')
        email = self.browser.find_element(by=By.NAME, value='email')
        email.send_keys('wrong@wrong.com')
        enter = self.browser.find_element(by=By.TAG_NAME, value='button')
        enter.click()
        assert self.browser.current_url == "http://127.0.0.1:5000/showSummary"
        element_h1 = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        assert element_h1 == "Welcome to the GUDLFT Registration Portal!"

    '''def test_signup_and_booking_places_and_logout(self, mock_clubs, mock_competitions):
        # login user
        self.browser = webdriver.Firefox(service=Service('tests/functional_tests/geckodriver'))
        self.browser.get('http://127.0.0.1:5000/')
        element = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        assert element == "Welcome to the GUDLFT Registration Portal!"
        email = self.browser.find_element(by=By.NAME, value='email')
        email.send_keys('john@simplylift.co')
        enter = self.browser.find_element(by=By.TAG_NAME, value='button')
        enter.click()
        assert self.browser.current_url == "http://127.0.0.1:5000/showSummary"
        element_h3 = self.browser.find_element(by=By.TAG_NAME, value='h3').text
        assert element_h3 == 'Competitions:'

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

    def tearDown(self):
        self.browser.close()
        self.browser.quit()'''
        '''dump_data("clubs.json", {"clubs": clubs})
        dump_data("competitions.json", {"competitions": competitions})
        dump_data("purchases.json", purchases)'''
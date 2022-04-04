from flask_testing import LiveServerTestCase
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from flask import url_for

from server import app


class TestUserTakesTheTest(LiveServerTestCase):

    def create_app(self):
        # Fichier de config uniquement pour les tests.
        app.config.from_object('tests.config')
        return app

    # Méthode exécutée avant chaque test
    def setUp(self):
        """Setup the test driver and create test users"""
        # Le navigateur est Firefox
        self.driver = webdriver.Chrome()

    # Méthode exécutée après chaque test
    def tearDown(self):
        self.driver.quit()

    def test_user_login(self):
        # On ouvre le navigateur avec l'adresse du serveur.
        self.driver.get(self.get_server_url())
        # L'adresse dans l'url doit être celle que l'on attend.
        # assert self.driver.current_url == 'http://localhost:5000/'

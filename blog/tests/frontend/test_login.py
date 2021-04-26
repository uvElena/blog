from .base import TestBase
from flask import url_for
import time


class TestLogin(TestBase):
    def setUp(self):
        super().setUp()
        self.driver.find_element_by_id("login_link").click()

    def user_login(self, user, password):
        self.driver.find_element_by_id("user_name").send_keys(user)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)

    def test_login(self):
        self.assertIn(url_for('main.login'), self.driver.current_url)

        self.user_login("user1", "1234")
        self.assertNotIn(url_for('main.login'), self.driver.current_url)

        full_name = self.driver.find_element_by_id("full_name").text
        self.assertEqual(full_name, "First Name Last Name")
        admin_link = self.driver.find_element_by_id("admin_link").text
        self.assertEqual(admin_link, "Admin")
        logout_link = self.driver.find_element_by_id("logout_link").text
        self.assertEqual(logout_link, "Sign out")

    def test_login_name_errors(self):
        self.user_login("TEST", "1234")
        user_name_errors = self.driver.find_element_by_id('user_name_errors').text
        self.assertNotEqual(user_name_errors, "")

    def test_login_password_errors(self):
        self.user_login("user1", "TEST")
        password_errors = self.driver.find_element_by_id('password_errors').text
        self.assertNotEqual(password_errors, "")

    def test_login_password_empty(self):
        self.user_login("user1", "")
        user_password_empty = self.driver.find_element_by_id("password").send_keys("")
        self.assertNotEqual(user_password_empty, "")

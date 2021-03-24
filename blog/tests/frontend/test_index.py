from .base import TestBase
from flask import url_for
import time


class TestView(TestBase):

    def test_index(self):
        title_text = self.driver.find_element_by_class_name("card-title").text
        self.assertEqual(title_text, "Post title")

        full_name = self.driver.find_element_by_id("full_name").text
        self.assertEqual(full_name, "First Name Last Name")

        summary = self.driver.find_element_by_tag_name('p').text
        self.assertEqual(summary, "Post summary")

    def test_view_post(self):
        self.driver.find_element_by_class_name("card-title").click()
        self.assertIn(url_for('main.post', id=1), self.driver.current_url)

        body = self.driver.find_element_by_css_selector("p.card-text").text
        self.assertEqual(body, "Post body")
        time.sleep(1)

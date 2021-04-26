from .base import TestBase
from blog.models import db, User, Post
from datetime import datetime
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
        time.sleep(1)
        self.assertIn(url_for('main.post', id=1), self.driver.current_url)

        body = self.driver.find_element_by_css_selector("p.card-text").text
        self.assertEqual(body, "Post body")

    def test_view_tags(self):
        post_count = len(self.driver.find_elements_by_class_name("card-title"))
        tag1 = self.driver.find_elements_by_class_name("tag_link")[0].text
        tag2 = self.driver.find_elements_by_class_name("tag_link")[1].text
        tags = [tag1, tag2]
        self.assertIn('tag1', tags)
        self.assertIn('tag2', tags)
        self.driver.find_element_by_css_selector("a.tag_link").click()
        time.sleep(1)
        post_count_tag = len(self.driver.find_elements_by_class_name("card-title"))
        self.assertLess(post_count_tag, post_count)

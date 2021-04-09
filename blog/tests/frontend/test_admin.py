from .base import TestBase
from flask import url_for
from selenium.common.exceptions import NoSuchElementException
import time


class TestAdmin(TestBase):
    def setUp(self):
        super().setUp()
        self.driver.find_element_by_id("login_link").click()
        self.driver.find_element_by_id("user_name").send_keys('user1')
        self.driver.find_element_by_id("password").send_keys("1234")
        self.driver.find_element_by_id("submit").click()

    def test_view_admin(self):
        admin_link = self.driver.find_element_by_id("admin_link").text
        self.assertEqual(admin_link, "Admin")

        self.driver.find_element_by_id("admin_link").click()
        self.assertIn(url_for('admin.index'), self.driver.current_url)

    def test_create_post(self):
        self.driver.find_element_by_id("admin_link").click()
        self.driver.find_element_by_id("create_post").click()

        self.assertIn(url_for('admin.post_edit', id=None), self.driver.current_url)

        self.driver.find_element_by_id("title").send_keys('TITLE')
        self.driver.find_element_by_id("summary").send_keys('SUMMARY')
        self.driver.find_element_by_id("body").send_keys('BODY')
        self.driver.find_element_by_id("submit").click()
        flash = self.driver.find_element_by_class_name('alert').text
        self.assertIn('created successfully', flash)
        time.sleep(1)

        self.driver.find_element_by_id('blog_link').click()
        time.sleep(1)
        title = self.driver.find_element_by_class_name("card-title").text
        self.assertEqual(title, "TITLE")

    def test_delete_post(self):
        self.driver.find_element_by_id("admin_link").click()

        self.driver.find_element_by_css_selector('button.btn-danger').click()
        time.sleep(1)

        danger_modal = self.driver.find_element_by_class_name('modal-body').text
        self.assertIn('delete', danger_modal)
        self.driver.find_element_by_css_selector('a.btn-danger').click()
        time.sleep(1)

        flash = self.driver.find_element_by_class_name('alert').text
        time.sleep(1)
        self.assertIn('Successfully deleted', flash)

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name("card-title")

    def test_update_post(self):
        self.driver.find_element_by_id("admin_link").click()
        self.driver.find_element_by_id("post_edit").click()
        self.assertIn(url_for('admin.post_edit', id=1), self.driver.current_url)

        self.driver.find_element_by_id("title").send_keys('TITLE UPDATED')
        self.driver.find_element_by_id("summary").send_keys('SUMMARY UPDATED')
        self.driver.find_element_by_id("body").send_keys('BODY UPDATED')
        self.driver.find_element_by_id("submit").click()
        flash = self.driver.find_element_by_class_name('alert').text
        time.sleep(1)
        self.assertIn('updated successfully', flash)

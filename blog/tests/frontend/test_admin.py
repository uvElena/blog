from .base import TestBase
from flask import url_for
import time


class TestAdmin(TestBase):
    def setUp(self):
        super().setUp()
        self.driver.find_element_by_id("login_link").click()
        self.driver.find_element_by_id("user_name").send_keys('user1')
        self.driver.find_element_by_id("password").send_keys("1234")
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)
        self.driver.find_element_by_id("admin_link").click()
        time.sleep(1)

    def test_view_admin(self):
        admin_link = self.driver.find_element_by_id("admin_link").text
        self.assertEqual(admin_link, "Admin")
        time.sleep(1)

        self.assertIn(url_for('admin.index'), self.driver.current_url)

    def test_create_post(self):
        self.driver.find_element_by_id("create_post").click()
        time.sleep(1)

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
        first_title_before_delete = self.driver.find_element_by_class_name("card-title").text

        self.driver.find_element_by_css_selector('button.btn-danger').click()
        time.sleep(1)

        danger_modal = self.driver.find_element_by_class_name('modal-body').text
        self.assertIn('delete', danger_modal)
        self.driver.find_element_by_css_selector('a.btn-danger').click()
        time.sleep(1)

        flash = self.driver.find_element_by_class_name('alert').text
        time.sleep(1)
        self.assertIn('Successfully deleted', flash)

        first_title_after_delete = self.driver.find_element_by_class_name("card-title").text
        self.assertNotEqual(first_title_before_delete, first_title_after_delete)

    def test_update_post(self):
        self.driver.find_element_by_class_name("card-title").click()
        time.sleep(1)

        self.assertIn(url_for('admin.post_edit', id=1), self.driver.current_url)

        self.driver.find_element_by_id("title").send_keys('/TITLE UPDATED')
        self.driver.find_element_by_id("summary").send_keys('/SUMMARY UPDATED')
        self.driver.find_element_by_id("body").send_keys('/BODY UPDATED')
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)
        flash = self.driver.find_element_by_class_name('alert').text
        time.sleep(1)
        self.assertIn('updated successfully', flash)

    def test_delete_tag(self):
        self.driver.find_elements_by_class_name("card-title")[1].click()
        time.sleep(1)

        tags = self.driver.find_elements_by_class_name("tag_value")

        tag_value_delete = tags[1].get_attribute("value")

        self.driver.find_elements_by_css_selector('input.btn-danger')[1].click()
        time.sleep(1)

        self.driver.find_element_by_id("submit").click()
        time.sleep(1)

        tags = self.driver.find_elements_by_class_name("tag_value")

        tag_values = [element.get_attribute("value") for element in tags]

        self.assertNotIn(tag_value_delete, tag_values)

    def test_create_tag(self):
        self.driver.find_elements_by_class_name("card-title")[1].click()
        time.sleep(1)

        self.driver.find_element_by_id("new_tag").send_keys('new tag')
        self.driver.find_element_by_id('append_tag').click()
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)

        flash = self.driver.find_element_by_class_name('alert').text
        time.sleep(1)
        self.assertIn('updated successfully', flash)

        tags = self.driver.find_elements_by_class_name("tag_value")

        tag_values = [element.get_attribute("value") for element in tags]
        self.assertIn('new tag', tag_values)

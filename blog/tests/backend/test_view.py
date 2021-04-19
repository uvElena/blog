from .base import TestBase
from flask import url_for


class TestView(TestBase):

    def test_index(self):
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        response = self.client.get(url_for('main.post', id=1))
        self.assertEqual(response.status_code, 200)

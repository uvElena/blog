from .base import TestBase
from flask import url_for


class TestLogin(TestBase):
    def test_login_view(self):
        response = self.client.get(url_for('main.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        target_url = url_for('main.logout')
        redirect_url = url_for('main.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_login_successful(self):
        response = self.client.post(
            'main/login',
            data={'user_name': 'user1', 'password': '1234'},
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(url_for('admin.index'))
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_user_name(self):
        response = self.client.post(
            '/login',
            data={'user_name': 'TEST', 'password': '1234'}
        )
        response = self.client.get(url_for('main.login'))
        self.assertEqual(response.status_code, 200)

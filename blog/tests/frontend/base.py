from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from flask_testing import LiveServerTestCase
from selenium import webdriver

from blog.app import create_app
from blog.models import db, User, Post
from blog.config import Configuration


class TestConfiguration(Configuration):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/blog.db'
    LIVESERVER_PORT = 8943
    TESTING = True


class TestBase(LiveServerTestCase):

    def create_app(self):
        app = create_app(TestConfiguration)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

        user = User(
            user_name="user1",
            first_name="First Name",
            last_name="Last Name",
            password=generate_password_hash("1234")
        )
        db.session.add(user)

        post = Post(
            title="Post title",
            summary="""Post summary""",
            body="""Post body""",
            author=user,
            created=datetime(2020, 1, 15, 10, 30) + timedelta(days=1),
            updated=datetime(2020, 1, 15, 10, 30) + timedelta(days=1),
            )
        db.session.add(post)
        db.session.commit()

        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()

import logging
import os
from datetime import datetime

from werkzeug.security import generate_password_hash
from flask_testing import LiveServerTestCase
from selenium import webdriver

from blog.app import create_app
from blog.models import db, User, Post, Tag
from blog.config import Configuration


class TestConfiguration(Configuration):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/blog.db'
    LIVESERVER_PORT = 8943
    TESTING = True
    DEBUG = False


class TestBase(LiveServerTestCase):

    def create_app(self):
        app = create_app(TestConfiguration)
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

        tag1 = Tag(
            value="tag1"
        )
        db.session.add(tag1)

        tag2 = Tag(
            value="tag2"
        )
        db.session.add(tag2)

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
            created=datetime(2020, 1, 15, 10, 30),
            updated=datetime(2020, 1, 15, 10, 30),
        )
        post_with_tags = Post(
            title="Second post title",
            summary="""Second post summary""",
            body="""Second post body""",
            author=user,
            created=datetime(2020, 1, 15, 10, 30),
            updated=datetime(2020, 1, 15, 10, 30),
            tags=[tag1, tag2]
        )

        db.session.add(post)
        db.session.add(post_with_tags)
        db.session.commit()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()

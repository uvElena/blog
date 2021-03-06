import logging
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from flask_testing import TestCase

from blog.app import create_app
from blog.models import db, User, Post
from blog.config import Configuration


class TestConfiguration(Configuration):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/blog.db'
    WTF_CSRF_ENABLED = False
    TESTING = True
    DEBUG = False


class TestBase(TestCase):

    def create_app(self):
        app = create_app(TestConfiguration)
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

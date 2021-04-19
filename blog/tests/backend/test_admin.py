from .base import TestBase
from flask import url_for
from blog.models import Post


class TestAdmin(TestBase):
    def setUp(self):
        super().setUp()
        self.client.post(
            'main/login',
            data={'user_name': 'user1', 'password': '1234'},
        )

    def test_post_delete(self):
        post = Post.query.first()
        self.client.get(url_for('admin.post_delete', id=post.id))
        post = Post.query.filter(Post.id == post.id).first()
        self.assertEqual(post, None)
        self.assertEqual(Post.query.count(), 0)

    def test_post_edit(self):
        post = Post.query.first()
        self.client.post(
            url_for('admin.post_edit', id=post.id),
            data={'title': 'NEW TITLE', 'submit': True}
            )
        post = Post.query.filter(Post.id == post.id).first()
        self.assertEqual(post.title, "NEW TITLE")

    def test_post_new(self):
        self.client.post(
            url_for('admin.post_edit', id=None),
            data={'title': 'NEW POST', 'submit': True}
            )
        self.assertEqual(Post.query.count(), 2)

        post = Post.query.filter(Post.id == 2).one()
        self.assertEqual(post.title, "NEW POST")

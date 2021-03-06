from flask_login import login_required, login_user, logout_user
from flask import render_template, request, redirect, url_for
from flask import Blueprint, send_from_directory, current_app

from . import models
from . import forms

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/main', methods=['GET', 'POST'])
@main.route('/main<int:page>', methods=['GET', 'POST'])
def index(page=1):
    tag = request.args.get('tag', default='', type=str)

    tags = models.Tag.query.all()
    posts_query = models.Post.query
    if tag != '':
        posts_query = posts_query.filter(models.Post.tags.any(models.Tag.value == tag))

    posts_query = posts_query.order_by(models.Post.created.desc())
    posts = posts_query.paginate(page, 10, False)

    return render_template('main/index.html', posts=posts, tags=tags, tag=tag)


@main.route('/main/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = models.Post.query.filter(models.Post.id == id).one()

    return render_template('main/post.html', post=post)


@main.route('/main/login', methods=['GET', 'POST'])
def login():

    form = forms.LoginForm()

    if form.validate_on_submit():

        user = models.User.query.filter(models.User.user_name == form.user_name.data).one()

        login_user(user)

        return redirect(url_for('main.index'))

    return render_template('main/login.html', form=form)


@main.route("/main/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route("/main/img/<path:name>")
def image(name):
    return send_from_directory(
        current_app.config['IMAGE_FOLDER'], name
    )

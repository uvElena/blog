import models
import forms
from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from datetime import datetime

admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/admin<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):

    tag = request.args.get('tag', default='', type=str)

    tags = models.Tag.query.all()

    posts_query = models.Post.query
    if tag != '':
        posts_query = posts_query.filter(models.Post.tags.any(models.Tag.name == tag))

    posts_query = posts_query.order_by(models.Post.created.desc())
    posts = posts_query.paginate(page, 10, False)

    return render_template('admin/index.html', posts=posts, tags=tags)


@admin.route('/admin/create', methods=['GET', 'POST'])
@admin.route('/admin/post_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def post_edit(id=None):
    if id is None:
        post = models.Post(created=datetime.now(), author=current_user)
    else:
        post = models.Post.query.filter(models.Post.id == id).one()

    form = forms.Post(obj=post)

    t = None
    for tag in form.tags:
        if tag.pop_tag.data:
            t = tag
    if t is not None:
        form.tags.remove_entry(t)

    if form.append_tag.data and form.new_tag.data:
        new_tag = form.new_tag.data
        new_tag_form = forms.Tag()
        new_tag_form.value = new_tag
        form.tags.append_entry(new_tag_form)
        form.new_tag.data = ''

    if form.submit.data and form.validate_on_submit():

        form.populate_obj(post)

        models.db.session.add(post)
        models.db.session.commit()

        form_img = form.image.data
        form_img.save(f'static/img/{post.id}.jpg')
        return redirect(url_for('admin.post_edit', id=post.id))

    return render_template('admin/post_edit.html', post=post, form=form)


@admin.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def post_delete(id):

    post = models.Post.query.filter(models.Post.id == id).one()
    models.db.session.delete(post)
    models.db.session.commit()

    flash('Successfully deleted the post.')

    return redirect(url_for('admin.index'))

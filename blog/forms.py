from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList, PasswordField, FileField
from wtforms import validators
from wtforms_alchemy import model_form_factory
from werkzeug.security import check_password_hash

from . import models
from .models import db

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class TagsList(FieldList):
    def remove_entry(self, entry):
        self.entries.remove(entry)
        self.last_index -= 1

    def populate_obj(self, obj, name):
        tags = []
        for tag_form in self.entries:
            tag_value = tag_form.value.data
            tag = models.Tag.query.filter(models.Tag.value == tag_value).first()
            if tag is None:
                tag = models.Tag(value=tag_value)
            tags.append(tag)
        obj.tags = tags


class Tag(ModelForm):
    class Meta:
        model = models.Tag
        include_primary_keys = True
    pop_tag = SubmitField('Delete tag')


class Post(ModelForm):
    class Meta:
        model = models.Post
        include_foreign_keys = True
    new_tag = StringField('New tag')
    tags = TagsList(FormField(Tag, default=lambda: models.Tag()))
    append_tag = SubmitField('Add new tag')
    submit = SubmitField('Save')
    image = FileField('Image File')


class LoginForm(FlaskForm):
    user_name = StringField('Person code', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Login')

    def validate(self):
        if not super().validate():
            return False
        user = models.User.query.filter(models.User.user_name == self.user_name.data).first()
        if user is None:
            self.user_name.errors.append('Unknown user name')
            return False
        if not check_password_hash(user.password, self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True

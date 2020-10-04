from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

post_tag_table = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_value', db.String, db.ForeignKey('tag.value'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, name='PERSON ID', primary_key=True)
    person_code = db.Column(db.String(255), name='Person Code', info={'label': 'Person Code'})
    first_name = db.Column(db.String(255), name='FIRST NAME', info={'label': 'First name'})
    last_name = db.Column(db.String(255), name='LAST NAME', info={'label': 'Last name'})
    password = db.Column(db.String(255), name='Individual Password', info={'label': 'Password'})

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return '<ID: {}, {} {}>'.format(self.id, self.first_name, self.last_name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, name='Title', info={'label': 'Title'})
    summary = db.Column(db.Text, name='Summary', info={'label': 'Summary'})
    body = db.Column(db.Text, name='Body', info={'label': 'Body'})
    created = db.Column(db.DateTime)
    tags = db.relationship("Tag", secondary=post_tag_table)
    author = db.relationship('User')
    author_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)


class Tag(db.Model):
    value = db.Column(db.String(150), primary_key=True, info={'label': 'Tag'})

    def __repr__(self):
        return '<Tag value {}>'.format(self.value)

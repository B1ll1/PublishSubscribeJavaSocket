import os
from config import login_manager, app, db
from werkzeug.security import generate_password_hash, check_password_hash

class Publishing(db.Model):
    __tablename__ = 'publishings'
    id = db.Column('id', db.Integer, primary_key = True)
    topic = db.Column('topic', db.String(100))
    text = db.Column('text', db.Text(300))

    def __init__(self, topic, text):
        self.topic = topic
        self.text    = text

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Publishing $r>' % (self.topic)

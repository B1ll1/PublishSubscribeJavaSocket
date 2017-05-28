import os
from config import login_manager, app, db
from werkzeug.security import generate_password_hash, check_password_hash

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column('id', db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer)
    topic = db.Column('topic', db.String(100))

    def __init__(self, topic, user_id):
        self.topic = topic
        self.user_id = user_id

    def get_id(self):
        return unicode(self.id)

    def get_userId(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<Subscription $r>' % (self.topic)

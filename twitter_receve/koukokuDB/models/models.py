from datetime import datetime
from twitter_receve.koukokuDB.database import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    twitter_userid = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, twitter_userid):
        self.twitter_userid = twitter_userid

    def __repr__(self):
        return '<UserID %r>' % self.twitter_userid

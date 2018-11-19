from datetime import datetime
from DB.koukokuDB.database import db

class UserStatus(db.Model):

    __tablename__ = 'user_statuses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    info_1 = db.Column(db.Boolean, nullable=False)
    info_2 = db.Column(db.Boolean, nullable=False)
    info_3 = db.Column(db.Boolean, nullable=False)
    info_4 = db.Column(db.Boolean, nullable=False)
    info_5 = db.Column(db.Boolean, nullable=False)
    info_6 = db.Column(db.Boolean, nullable=False)
    info_7 = db.Column(db.Boolean, nullable=False)
    info_8 = db.Column(db.Boolean, nullable=False)
    info_9 = db.Column(db.Boolean, nullable=False)
    info_10 = db.Column(db.Boolean, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<UserID %r>' % self.user_id

from datetime import datetime
from DB.koukokuDB.database import db

class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    recommen_item_id = db.Column(db.Integer, db.ForeignKey('recommen_items.id'))
    feedback = db.Column(db.Integer, nullable=False)
    learned_flag = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, user_id, recommen_item_id, feedback):
        self.user_id = user_id
        self.recommen_item_id = recommen_item_id
        self.feedback = feedback

    def __repr__(self):
        return '<FeedbackUserID %r>' % self.user_id

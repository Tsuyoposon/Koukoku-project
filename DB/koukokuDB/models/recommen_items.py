from datetime import datetime
from DB.koukokuDB.database import db

class Recommen_item(db.Model):

    __tablename__ = 'recommen_items'

    id = db.Column(db.Integer, primary_key=True)
    recommen_item_name = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, id, recommen_item_name):
        self.id = id
        self.recommen_item_name = recommen_item_name

    def __repr__(self):
        return '<recommen_item_name %r>' % self.recommen_item_name

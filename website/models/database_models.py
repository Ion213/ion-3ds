from website import db
from sqlalchemy.sql import func
from pytz import timezone
import datetime

manila_tz = timezone('Asia/Manila')

#parent of event fees,payments,attendance
class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name=db.Column(db.String(255),nullable=False)
    links = db.relationship('Links', backref='games', lazy=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=manila_tz))



class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)

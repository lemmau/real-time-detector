from app import db
from src.Object import Object

dailyReportTable = db.Table('DailyObject',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('eventId', db.Integer, db.ForeignKey('DailyReport.id')),
    db.Column('objectId', db.Integer, db.ForeignKey('Object.id')),
    db.Column('count', db.Integer, nullable=False),
    db.Column('isDeleterd', db.Boolean, default=False),
)

class DailyReport(db.Model):

    __tablename__ = 'DailyReport'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DateTime, nullable=False)
    infractions = db.Column(db.Integer, nullable=False)
    events = db.Column(db.Integer, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
   

from app import db
from src.DetectedClass import DetectedClass


class DailyReport(db.Model):

    __tablename__ = 'DailyReport'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DateTime, nullable=False)
    infractions = db.Column(db.Integer, nullable=False)
    events = db.Column(db.Integer, nullable=False)
    detectedClassId = db.relationship('DetectedClass')
    isDeleted = db.Column(db.Boolean, default=False)
   

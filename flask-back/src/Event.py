from app import db
from src.DetectedClass import DetectedClass

class Event(db.Model):

    __tablename__ = 'Event'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, nullable=False)
    detectedClassId = db.Column(db.Integer, db.ForeignKey('DetectedClass.id'))
    isInfraction = db.Column(db.Boolean, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)

    detectedClass = db.relationship('DetectedClass')

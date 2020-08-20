from app import db
from src.Object import Object

eventObjectTable = db.Table('EventObject',
    db.Column('eventId', db.Integer, db.ForeignKey('Event.id')),
    db.Column('objectId', db.Integer, db.ForeignKey('Object.id')),
    db.Column('isDeleted', default=False)
)

class Event(db.Model):

    __tablename__ = 'Event'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, nullable=False)
    objectId = db.relationship('Object', secondary=eventObjectTable)
    isInfaction = db.Column(db.Boolean, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)

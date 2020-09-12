from src.DetectedClass import DetectedClass
from sqlalchemy.orm import sessionmaker
from src.DBHelper import *
from core.definitions import INFRACTION_ID
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):

    __tablename__ = 'Event'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, nullable=False)
    # detectedClassId = db.Column(db.Integer, db.ForeignKey('DetectedClass.id'))
    detectedClassId = db.Column(db.Integer, nullable=False)
    isInfraction = db.Column(db.Boolean, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)

    # detectedClass = db.relationship('DetectedClass')

    def __init__(self, timestamp, detectedClassId, isInfraction):
        self.timestamp = timestamp
        self.detectedClassId = detectedClassId
        self.isInfraction = isInfraction

    @staticmethod
    def processAndPersistEvent(detectedClassesPrevious, currentDetectedClasses, timestamp, app):
        if (Event.shouldPersistEvents(detectedClassesPrevious, currentDetectedClasses)):
            with app.app_context():
                Session = sessionmaker()
                Session.configure(bind=db.engine)
                session = Session()

                newClasses = Event.Diff(detectedClassesPrevious, currentDetectedClasses)

                for newClass in newClasses:

                    if(detectedClassesPrevious != None):
                        print('Previous')
                        print([c.label for c in detectedClassesPrevious])
                    if(currentDetectedClasses != None):
                        print('Current')
                        print([c.label for c in currentDetectedClasses])

                    print('New class to be saved')
                    print(newClass.label)

                    print('-------------------')

                    # save(session, Event(timestamp, newClass.id, newClass.id == INFRACTION_ID))

    @staticmethod
    def shouldPersistEvents(detectedClassesPrevious, currentDetectedClasses):
        noneCurrent = currentDetectedClasses == None
        nonePrevious = detectedClassesPrevious == None and not noneCurrent
        moreClassesOnCurrent = not nonePrevious and len(detectedClassesPrevious) < len(currentDetectedClasses)

        return not noneCurrent and (nonePrevious or moreClassesOnCurrent)

    @staticmethod
    def Diff(list1, list2):
        if list1 == None:
            return list2
        else:
            return (list(list(set(list1)-set(list2)) + list(set(list2)-set(list1))))

from datetime import datetime
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
    def processAndPersistEvent(detectedClassesPrevious, currentDetectedClasses, persistInfractions:bool, app):
        if (Event.shouldPersistEvents(detectedClassesPrevious, currentDetectedClasses)):
            with app.app_context():
                Session = sessionmaker()
                Session.configure(bind=db.engine)
                session = Session()

                newClasses = Event.Diff(detectedClassesPrevious, currentDetectedClasses)

                if not persistInfractions:
                    newClasses = list(filter(lambda detectedClass: detectedClass.id != INFRACTION_ID, newClasses))
                    print(newClasses)

                timestamp = datetime.timestamp(datetime.now())

                for newClass in newClasses:                        
                    print('New detection to be saved: ', newClass.label)
                    save(session, Event(timestamp, newClass.id, newClass.id == INFRACTION_ID))
    
    # @staticmethod
    # def persistInfraction(detectedClassesPrevious, currentDetectedClasses, app):
    #     timestamp = datetime.timestamp(datetime.now())

    #     with app.app_context():
    #         Session = sessionmaker()
    #         Session.configure(bind=db.engine)
    #         session = Session()

    #         print('New detection to be saved: Infraccion')
    #         save(session, Event(timestamp, INFRACTION_ID, True))


    @staticmethod
    def shouldPersistEvents(detectedClassesPrevious, currentDetectedClasses):
        noneCurrent = currentDetectedClasses == None
        moreClassesOnCurrent = not noneCurrent and len(detectedClassesPrevious) < len(currentDetectedClasses)
        newClassDetected = len(detectedClassesPrevious) == len(currentDetectedClasses) and detectedClassesPrevious != currentDetectedClasses

        return not noneCurrent and (moreClassesOnCurrent or newClassDetected)

    @staticmethod
    def Diff(list1, list2):
        if list1 == None:
            return list2
        else:
            # return (list(list(set(list1)-set(list2)) + list(set(list2)-set(list1))))
            return list(set(list2)-set(list1))

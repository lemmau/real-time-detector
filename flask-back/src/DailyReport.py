from src.DetectedClass import DetectedClass
from flask_sqlalchemy import SQLAlchemy
from src.DBHelper import *
from datetime import datetime, timedelta

db = SQLAlchemy()

class DailyReport(db.Model):

    __tablename__ = 'DailyReport'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DateTime, nullable=False)
    events = db.Column(db.Integer, nullable=False)
    # detectedClassId = db.relationship('DetectedClass')
    detectedClassId = db.Column(db.Integer, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)

    def __init__(self, day, events, detectedClassId):
        self.day = day
        self.events = events
        self.detectedClassId = detectedClassId

    @staticmethod
    def runSync(db, session):
        print('Run dailyReport sync triggered')

        endTime = datetime.now()
        startTime = endTime - timedelta(hours=24)

        # allClasses = getAllClasses()
        allEventsLast24hsByClass = getEventsByClass(db, startTime, endTime)

        dailyReportsRowsToAdd = []

        for eventsByClass in allEventsLast24hsByClass:
            #TODO add suport for hour
            if allEventsLast24hsByClass[eventsByClass]:
                events = len(allEventsLast24hsByClass[eventsByClass])
                #TODO format day for sqlAlchemy
                day = datetime.fromtimestamp(allEventsLast24hsByClass[eventsByClass][0].timestamp)
                detectedClassId = allEventsLast24hsByClass[eventsByClass][0].detectedClassId

                dailyReportsRowsToAdd.append(
                    DailyReport(day, events, detectedClassId))

        saveBatch(session, dailyReportsRowsToAdd)

        print('DailyReport sync finished - Amount updated rows: ',
              leng(dailyReportsRowsToAdd))

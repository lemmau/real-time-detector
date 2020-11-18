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
        try:
            print('Run dailyReport sync triggered')

            endTime = datetime.now()
            startTime = endTime - timedelta(hours=24)

            # drop old DailyReport rows that will be updated
            sqlDropOldRows = """DELETE FROM DailyReport WHERE unix_timestamp(day) >= {oneDayAgo}
                                """.format(oneDayAgo=int(startTime.timestamp()))

            db.engine.execute(sqlDropOldRows)

            allEventsLast24hsByClass = getEventsByClass(db, startTime, endTime)

            dailyReportsRowsToAdd = []

            for eventsByClass in allEventsLast24hsByClass:
                for hour in range(24):
                    eventsInHour = list(filter(lambda event: int(datetime.fromtimestamp(event.timestamp).strftime("%H")) == hour, allEventsLast24hsByClass[eventsByClass]))

                    if len(eventsInHour) > 0:
                        events = len(eventsInHour)
                        day = datetime.fromtimestamp(eventsInHour[0].timestamp).strftime("%Y-%m-%d %H:00:00")
                        detectedClassId = eventsInHour[0].detectedClassId

                        dailyReportsRowsToAdd.append(DailyReport(day, events, detectedClassId))

            saveBatch(session, dailyReportsRowsToAdd)

            print('DailyReport sync finished')
        except:
            print('DailyReport sync failed')


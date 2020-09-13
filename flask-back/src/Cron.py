from core.definitions import FIRST_DAY_MONTH_SPANISH, LAST_DAY_MONTH_SPANISH, FIRST_DAY_MONTH_CRON, LAST_DAY_MONTH_CRON
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cron(db.Model):

    __tablename__ = 'Cron'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    day = db.Column(db.String(10), nullable=False)
    hour = db.Column(db.String(2), nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
    
    def __init__(self, date, day_of_week, day, hour, isDeleted):
        self.date = date
        self.day_of_week = day_of_week
        self.day = day
        self.hour = hour
        self.isDeleted = isDeleted

    @staticmethod
    def translateDayOfWeek(dayOfWeek):
        days = {
            'lunes': 'mon',
            'martes': 'tue',
            'miercoles': 'wed',
            'jueves': 'tue',
            'viernes': 'fri',
            'sabado': 'sat',
            'domingo': 'sun'
        }

        return days.get(dayOfWeek.lower(), None)

    @staticmethod
    def calculateDayOfMonth(dayOfMonth):
        daysOfMonth = {
            FIRST_DAY_MONTH_SPANISH: FIRST_DAY_MONTH_CRON,
            LAST_DAY_MONTH_SPANISH: LAST_DAY_MONTH_CRON
        }

        return daysOfMonth.get(dayOfMonth, None)

from core.definitions import FIRST_DAY_MONTH_SPANISH, LAST_DAY_MONTH_SPANISH, FIRST_DAY_MONTH_CRON, LAST_DAY_MONTH_CRON
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cron(db.Model):

    __tablename__ = 'Cron'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    frecuency = db.Column(db.String(20), nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
    
    def __init__(self, date, frecuency, isDeleted):
        self.date = date
        self.frecuency = frecuency
        self.isDeleted = isDeleted

    @staticmethod
    def translateDayOfWeek(dayOfWeek):
        days = {
            'lunes': "1",
            'martes': "2",
            'miercoles': "3",
            'jueves': "4",
            'viernes': "5",
            'sabado': "6",
            'domingo': "0"
        }

        return days.get(dayOfWeek, None)

    @staticmethod
    def calculateDayOfMonth(dayOfMonth):
        daysOfMonth = {
            FIRST_DAY_MONTH_SPANISH: FIRST_DAY_MONTH_CRON,
            LAST_DAY_MONTH_SPANISH: LAST_DAY_MONTH_CRON
        }

        return daysOfMonth.get(dayOfMonth, None)

import time
import calendar
import csv
import os
from datetime import datetime, timedelta
from src.SendMail import SendMail
from src.DetectedClass import DetectedClass
from dateutil import rrule
from src.Email import Email

class EmailSender:

    @staticmethod
    def triggerEmailSender(frecuency, now, db, app):
        startDay = now - timedelta(days = 7) if frecuency['frecuency'] == 'weekly' else EmailSender.monthdelta(now, -1)
        startDay = startDay.strftime("%Y-%m-%d")
        endDay = now.strftime("%Y-%m-%d")

        sql = f"""SELECT date_format(dr.day, '%%Y-%%m-%%d') day, date_format(dr.day, '%%H') hour, dc.name, dr.events FROM DailyReport dr
                JOIN DetectedClass dc ON dc.id = dr.detectedClassId
                WHERE date_format(dr.day, '%%Y-%%m-%%d') >= '{startDay}'
                AND date_format(dr.day, '%%Y-%%m-%%d') <= '{endDay}'
                ORDER BY dr.day"""

        queryResult = db.engine.execute(sql)

        fileName = EmailSender.generateEmail(queryResult, startDay, endDay)
        message = 'RTD - Reporte correspondiente a las detecciones entre {0} y {1}'.format(startDay, endDay)
        subject = 'RTD - Reporte {0} - {1}'.format(startDay, endDay)
        
        with app.app_context():
            emailList = list(map(lambda email: email.email, Email.query.all()))

        SendMail.sendMailTo(emailList, subject, message, [fileName])
        
        if os.path.exists(fileName):
            os.remove(fileName)

        print('Reporte enviado: %s' % datetime.now())

    @staticmethod
    def monthdelta(date, delta):
        m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
        if not m: m = 12
        d = min(date.day, calendar.monthrange(y, m)[1])

        return date.replace(day=d,month=m, year=y)

    @staticmethod
    def generateEmail(queryResult, startDay, endDay):
        dbInfo = {
            'Barbijo': [],
            'Limpio': [],
            'Protección ocular': [],
            'Mascara Facial': [],
            'Barbijo y Protección ocular': []
        }

        fileName = 'reporte_{0}-{1}.csv'.format(startDay, endDay)
        with open(fileName, 'w', newline='') as file:
            writer = csv.writer(file)

            for row in queryResult:
                dbInfo[row['name']].append(row)

            for element in dbInfo:
                if len(dbInfo[element]) > 0:
                    writer.writerow([element])
                    writer.writerow(["DIA", "HORA", "EVENTOS"])
                    
                    for row in dbInfo[element]:
                        writer.writerow([row['day'], row['hour'] + ':00', row['events']])
                    
                    writer.writerow(['----------------------'])

        return fileName

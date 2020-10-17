from src.Email import Email
from sqlalchemy import update
from src.DetectedClass import DetectedClass
from datetime import datetime

def save(session, asset):
    session.add(asset)
    session.commit()

def deleteEmail(session, asset):
    session.query(Email).filter(Email.email == asset).update({Email.isDeleted:True}, synchronize_session = False)

    session.commit()

def restoreEmail(session, asset):
    session.query(Email).filter(Email.email == asset).update({Email.isDeleted:False}, synchronize_session = False)

    session.commit()

def getAllEmailsAvailables(session, app):
    with app.app_context():
        emailList = list(Email.query.all())

        return map(lambda email: email.email, filter(lambda email: email.isDeleted == False, emailList))

def getAllEmails(session, app):
    with app.app_context():
        emailList = list(Email.query.all())

        return emailList

def getAllClasses():
    return DetectedClass.query.all()

def getEventsByClass(db, startTime, endTime):
    startTimestamp = datetime.timestamp(startTime)
    endTimestamp = datetime.timestamp(endTime)
        
    dbInfo = {
        'Barbijo': [],
        'Limpio': [],
        'Protección ocular': [],
        'Mascara Facial': [],
        'Barbijo y Protección ocular': []
    }

    sql = f"""SELECT * FROM Event e
        JOIN DetectedClass dc ON dc.id = e.detectedClassId
        WHERE e.timestamp >= {startTimestamp}
        AND e.timestamp <= {endTimestamp}
        ORDER BY e.timestamp"""

    queryResult = db.engine.execute(sql)

    for row in queryResult:
        dbInfo[row['name']].append(row)

    return dbInfo

def getStatisticsOfToday(dbContext):

    sql = f"""SELECT date_format(from_unixtime(e.timestamp), '%%H') hour, dc.name, count(*) events FROM Event e
                JOIN DetectedClass dc ON dc.id = e.detectedClassId
                WHERE date_format(from_unixtime(e.timestamp), '%%Y-%%m-%%d') = CURDATE() AND e.isDeleted = 0
                GROUP BY date_format(from_unixtime(e.timestamp), '%%H'), dc.name
            """

    return dbContext.engine.execute(sql)

def getStatisticsByDate(dbContext, date):

    if date == datetime.today().strftime('%Y-%m-%d'):
        return getStatisticsOfToday(dbContext)
    else:
        sql = f"""SELECT date_format(dr.day, '%%H') hour, dc.name, dr.events FROM DailyReport dr
                JOIN DetectedClass dc ON dc.id = dr.detectedClassId
                WHERE date_format(dr.day, '%%Y-%%m-%%d') = '{date}'
                ORDER BY dr.day"""

    return dbContext.engine.execute(sql)

def saveBatch(session, elementsToSave):
    session.add_all(elementsToSave)
    session.commit()

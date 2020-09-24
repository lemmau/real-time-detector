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

def saveBatch(session, elementsToSave):
    session.add_all(elementsToSave)
    session.commit()

from src.DetectedClass import DetectedClass
from datetime import datetime

def save(session, asset):
    session.add(asset)
    session.commit()

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

    # sql = f"""SELECT * FROM Event e
    #     JOIN DetectedClass dc ON dc.id = e.detectedClassId
    #     WHERE e.timestamp >= '{startTimestamp}'
    #     AND e.timestamp <= '{endTimestamp}'
    #     ORDER BY e.timestamp"""
    sql = f"""SELECT * FROM Event e
        JOIN DetectedClass dc ON dc.id = e.detectedClassId
        WHERE e.timestamp >= 1599921493
        AND e.timestamp <= 1599944227
        ORDER BY e.timestamp"""

    queryResult = db.engine.execute(sql)

    for row in queryResult:
        dbInfo[row['name']].append(row)

    return dbInfo

def saveBatch(session, elementsToSave):
    session.add_all(elementsToSave)
    session.commit()
from src.Email import Email
from sqlalchemy import update

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


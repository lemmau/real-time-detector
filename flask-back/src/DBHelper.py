from src.Email import Email

def save(session, asset):
    session.add(asset)
    session.commit()

def getAllEmails(session, app):
    with app.app_context():
        emailList = list(Email.query.all())

        return map(lambda email: email.email, filter(lambda email: email.isDeleted == False, emailList))


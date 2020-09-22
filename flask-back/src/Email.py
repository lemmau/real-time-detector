from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Email(db.Model):

    __tablename__ = 'Email'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)

    def __init__(self, email, isDeleted=False):
        self.email = email
        self.isDeleted = isDeleted


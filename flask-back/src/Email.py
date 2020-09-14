from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Email(db.Model):

    __tablename__ = 'Email'

    id = db.Column(db.Integer, primary_key=True)
    cronId = db.Column(db.Integer, db.ForeignKey('Cron.id'))
    email = db.Column(db.String(200), nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)

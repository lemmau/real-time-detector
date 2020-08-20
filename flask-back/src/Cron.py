from app import db

class Cron(db.Model):

    __tablename__ = 'Cron'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    frecuency = db.Column(db.String(10), nullable=False)
    operationType = db.Column(db.Integer, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
    
    emailSubscriptions = db.relationship("Email")

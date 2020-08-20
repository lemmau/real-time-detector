from app import db

class Object(db.Model):

    __tablename__ = 'Object'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)

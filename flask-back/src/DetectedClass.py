from app import db

class DetectedClass(db.Model):

    __tablename__ = 'DetectedClass'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)

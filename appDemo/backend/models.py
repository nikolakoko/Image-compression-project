from datetime import datetime

from database import db


class CompressionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    method = db.Column(db.String(20), nullable=False)
    quality = db.Column(db.Integer, nullable=True)
    k_value = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

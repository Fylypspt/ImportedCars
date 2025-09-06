from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quotes = db.relationship('Quote', backref='user', lazy=True)


def __repr__(self):
    return f'<User {self.phone}>'


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_info = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(20), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    cilindrada = db.Column(db.String(50), nullable=True)
    ano = db.Column(db.String(4), nullable=True)
    combustivel = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
    return f'<Quote {self.id} for user {self.user_id}>'
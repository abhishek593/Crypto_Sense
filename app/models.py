import datetime
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from flask import current_app
from time import time


@login_manager.user_loader
def load_user(user_id):
    return UserProfile.query.get(user_id)


class UserProfile(db.Model, UserMixin):
    __tablename__ = 'UserProfile'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(10), unique=True, index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Integer, default=1000)
    coin_investments = db.relationship('Investment', backref='UserProfile', lazy=True)

    def __init__(self, username, email, first_name, password, last_name=None, date_of_birth=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if date_of_birth:
            self.date_of_birth = date_of_birth
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'User {}'.format(self.username)

    def get_reset_password_token(self, expires_in=1000):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return UserProfile.query.get(id)


class Investment(db.Model):
    __tablename__ = 'Investment'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('UserProfile.id'), nullable=False)
    coin_name = db.Column(db.String, nullable=False)
    number_of_coins = db.Column(db.Float, default=0)
    date_last_updated = db.Column(db.Date, nullable=False,
                                  onupdate=datetime.datetime.now())
    total_price = db.Column(db.Float, default=0)
    coin_transactions = db.relationship('Transaction', backref='Investment', lazy=True)

    def __init__(self, user_id, coin_name, number_of_coins, total_price):
        self.user_id = user_id
        self.coin_name = coin_name
        self.number_of_coins = number_of_coins
        self.date_last_updated = datetime.datetime.now()
        self.total_price = total_price

    def __repr__(self):
        user = UserProfile.query.get(self.user_id)
        return 'User {} has {} coins of {}'.format(user.username, self.number_of_coins, self.coin_name)


class Transaction(db.Model):
    __tablename__ = 'Transaction'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    investment_id = db.Column(db.Integer, db.ForeignKey('Investment.id'), nullable=False)
    coin_name = db.Column(db.String(), nullable=False)
    number_of_coins = db.Column(db.Float, default=0)
    date = db.Column(db.Date, nullable=False, onupdate=datetime.datetime.now())
    total_price = db.Column(db.Float, default=0)

    def __init__(self, investment_id, coin_name, number_of_coins, total_price):
        self.investment_id = investment_id
        self.coin_name = coin_name
        self.number_of_coins = number_of_coins
        self.date = datetime.datetime.now()
        self.total_price = total_price

    def __repr__(self):
        investment = Investment.query.get(self.investment_id)
        user = UserProfile.query.get(investment.user_id)
        return 'User {} had transaction of {}'.format(user.username, self.total_price)

from app import db,models
from flask_login import UserMixin
from sqlalchemy.orm import relationship

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy

user_game = db.Table('user_game',
    db.Column('user_id', db.Integer, db.ForeignKey('useraccounts.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('boardgames.id'), primary_key=True)
)

class userAccount(UserMixin, db.Model):
    __tablename__= "useraccounts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    boardGames = db.relationship('boardGame', secondary=user_game, backref='accounts', order_by='boardGame.id')

class boardGame(db.Model):
    __searchable__ = ['body']
    __tablename__= "boardgames"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    minPlayers = db.Column(db.Integer)
    maxPlayers = db.Column(db.Integer)
    playTime = db.Column(db.Integer)
    releaseYear = db.Column(db.Integer)
    rating = db.Column(db.Float)
    imageURL = db.Column(db.String())
    minAge = db.Column(db.Integer)
    category = db.Column(db.String())


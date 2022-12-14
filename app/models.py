from app import db,models
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import event
import csv

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
    saves = db.Column(db.Integer)

#For when the database needs to be reset so the database is automatically repopulated with board games from CSV file
@event.listens_for(boardGame.__table__,'after_create')
def populateDatabase(*args, **kwargs):
    with open("goodBGDataset.csv") as file:
        reader = csv.reader(file)
        header = next(reader)

        for i,row in enumerate(reader):
            p = models.boardGame(
                id=i+1,
                title=row[0],
                minPlayers=int(row[1]),
                maxPlayers=int(row[2]),
                playTime=int(row[3]),
                releaseYear=int(row[4]),
                rating=float(row[5]),
                imageURL=row[6],
                minAge=int(row[7]),
                category=row[8],
                saves=0)
            db.session.add(p)
        db.session.commit()
import csv
from app import db,models

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
            category=row[8])
        db.session.add(p)
    db.session.commit()
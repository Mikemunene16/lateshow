from random import choice as rc

from app import app
from datetime import date
from models import db, Episode, Appearance, Guest

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()

        print("Seeding guests...")
        guests = [
            Guest(name="Michael J. Fox", occupation="Actor"),
            Guest(name="Sandra Bernhard", occupation="Comedian"),
            Guest(name="Tracy Ullman", occupation="Television Actress"),
            Guest(name="Gillian Anderson", occupation="Film Actress"),
            Guest(name="David Alan Grier", occupation="Actor"),
            Guest(name="William Baldwin", occupation="Actor"),
            Guest(name="Michael Stipe", occupation="Singer-Lyricist"),
            Guest(name="Carmen Electra", occupation="Model"),
            Guest(name="Matthew Lillard", occupation="Actor"),
            Guest(name="David Cross", occupation="Stand-Up Comedian"),
        ]
        db.session.add_all(guests)

        print("Seeding episodes...")
        episodes = [
            Episode(date=date(1999,1,11), number=1),
            Episode(date=date(1999,1,12), number=2),
            Episode(date=date(1999,1,13), number=3),
            Episode(date=date(1999,1,14), number=4),
            Episode(date=date(1999,1,18), number=5),
            Episode(date=date(1999,1,19), number=6),
            Episode(date=date(1999,1,20), number=7),
            Episode(date=date(1999,1,21), number=8),
            Episode(date=date(1999,1,25), number=9),
            Episode(date=date(1999,1,26), number=10),
        ]
        db.session.add_all(episodes)

        print("Seeding appearances...")
        appearances = []
        for episode in episodes:
            for _ in range(2):
                guest = rc(guests)
                rating = rc([1, 2, 3, 4, 5])
                appearances.append(Appearance(episode=episode, guest=guest, rating=rating))
        db.session.add_all(appearances)
        db.session.commit()

        print("Done seeding!")
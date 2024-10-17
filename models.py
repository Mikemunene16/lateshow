from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)


db = SQLAlchemy(metadata=metadata)


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'


    # serialize_only = ('date', 'id', 'number',)
    serialize_rules = ('-appearances.episode',)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    appearances = db.relationship('Appearance', back_populates='episode', cascade="all, delete-orphan")

    # Association proxy to get guests for this episode through appearances
    guests = association_proxy('appearances', 'guest',
                                 creator=lambda guest_obj: Appearance(guest=guest_obj))

    def __repr__(self):
        return f'<Episode id: {self.id}, date: {self.date}, number: {self.number}>'


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'


    serialize_rules = ('-appearances.guest',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String, nullable=False)

   
    appearances = db.relationship('Appearance', back_populates='guest', cascade="all, delete-orphan")

    # Association proxy to get episodes for this guest through appearances
    episodes = association_proxy('appearances', 'episode',
                                  creator=lambda episode_obj: Appearance(episode=episode_obj))

    def __repr__(self):
        return f'<Guest id: {self.id}, name: {self.name}, occupation: {self.occupation}>'


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    serialize_rules = ('-episode.appearances', '-guest.appearances',)

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    @validates('rating')
    def validate_strength(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError("The rating should be a value between 1 and 5 inclusive")
        return rating


    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    def __repr__(self):
        return f'<Appearance id:{self.id}, rating: {self.rating}, episode_id{self.episode_id}, guest_id{self.guest_id}>'
from flask_sqlalchemy import SQLAlchemy

import datetime

from pytz import timezone
db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent=db.Column(db.Boolean,nullable=False,default=False)
    seeking_description=db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String(120)))
    shows=db.relationship('Show', backref='venue',lazy=True)
    date_added=db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    def __repr__(self):
        return f'<Venue {self.phone} {self.name} {self.city}>'
    # date_added=db.Column(db.DateTime,default=datetime.datetime.now())
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):#parent artist can have many shows
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue=db.Column(db.Boolean,nullable=False,default=False)
    seeking_description=db.Column(db.String())
    shows=db.relationship('Show', backref='artist',lazy=True)
    genres = db.Column(db.ARRAY(db.String(120)))
    date_added=db.Column(db.DateTime(timezone=True),server_default=db.func.now())
    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.date_added}'

class Show(db.Model): #child show can only have one artist / venue per time

    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id=db.Column(db.Integer,db.ForeignKey('artists.id'),nullable=False)
    venue_id=db.Column(db.Integer,db.ForeignKey('venues.id'),nullable=False)
    start_time=db.Column(db.DateTime, default=db.func.now())
    def __repr__(self):
        return f'<Show {self.id} artist:{self.artist_id} venue:{self.venue_id} {self.start_time}'
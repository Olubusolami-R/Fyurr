from datetime import datetime

from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Optional, Regexp
from enums import Genre, State


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()], choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', 
        validators=
                [Optional(), Regexp('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$', message="Invalid number format, use: xxx-xxx-xxxx")]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(),URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(),URL()]
    )
    website_link = StringField(
        'website_link', validators=[Optional(),URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent',false_values=(False,'n'))

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    phone = StringField(
        # TODO implement validation logic for phone 
        'phone',
        validators=
                [Optional(),Regexp('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$',message="Invalid number format, use: xxx-xxx-xxxx")]
    )
    image_link = StringField(
        'image_link',validators=[DataRequired()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
     )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(),URL()]
     )

    website_link = StringField(
        'website_link',
        validators=[Optional(),URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue',false_values=(False,'n') )

    seeking_description = StringField(
            'seeking_description'
     )


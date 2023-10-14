#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
from xxlimited import new
import dateutil.parser
import babel
from flask import (
    Flask,
    jsonify, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db,Artist,Venue,Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
app.app_context().push()
db.init_app(app)
moment = Moment(app)
migrate=Migrate(app,db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  recent_venues=[]
  recent_artists=[]
  recent_artists=Artist.query.order_by(desc('date_added')).limit(10).all()
  recent_venues=Venue.query.order_by(desc('date_added')).limit(10).all()
  return render_template('pages/home.html',recent_artists=recent_artists,recent_venues=recent_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  areas=[]
  all_venues=Venue.query.all()
  venue_set=set()
  count=0

  for venue in all_venues:
    area_list=(venue.city,venue.state)
    if area_list not in venue_set:
      venue_set.add(area_list)
      areas.append({})
      areas[count]['city']=venue.city
      areas[count]['state']=venue.state
      areas[count]['venues']=[]
      count+=1

  for area in areas:
    for venue in all_venues:
      if area['city']==venue.city and area['state']==venue.state:
        area['venues'].append(venue)
  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term=request.form.get('search_term')
  response=Venue.query.filter(Venue.name.ilike('%'+search_term+'%')
                              |Venue.city.ilike('%'+search_term+'%')
                              | Venue.state.ilike('%'+search_term+'%')).all()
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive. Done
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue=Venue.query.get(venue_id)
  past_shows=Show.query.join(Venue).filter(Venue.id==venue_id).filter(Show.start_time<datetime.now())
  upcoming_shows=Show.query.join(Venue).filter(Venue.id==venue_id).filter(Show.start_time>datetime.now())
  return render_template('pages/show_venue.html', venue=venue, past_shows=past_shows, upcoming_shows=upcoming_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error=""
  form=VenueForm(request.form)
  if form.validate():
    try:
      newVenue=Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        image_link=form.image_link.data,
        phone=form.phone.data,
        address=form.address.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data, 
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
      )
      print(newVenue,newVenue.seeking_talent)
      db.session.add(newVenue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
      return redirect(url_for('index'))
  else:
    #to get specific validation errors
    for name, errorMessages in form.errors.items():
      for err in errorMessages:
        print(name,err)
        error+=name+": "+err+"\n"
    flash('An error occurred.'+error)

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  error=False
  venue=Venue.query.get(venue_id)
  print(venue)
  try:
    for show in venue.shows:
      db.session.delete(show)
    db.session.delete(venue)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()  
    if not error:  
      return jsonify({'status':'deleted'})
    else:
      return jsonify({'status':'not deleted'})


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  real_artists=Artist.query.all()
  return render_template('pages/artists.html', artists=real_artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term')
  response=Artist.query.filter(Artist.name.ilike('%'+search_term+'%')
                              |Artist.city.ilike('%'+search_term+'%')
                              |Artist.state.ilike('%'+search_term+'%')).all()
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  real_artist=Artist.query.get(artist_id)
  ps=Show.query.join(Artist).filter(Artist.id==artist_id).filter(Show.start_time<datetime.now())
  us=Show.query.join(Artist).filter(Artist.id==artist_id).filter(Show.start_time>datetime.now())
  return render_template('pages/show_artist.html', artist=real_artist,upcoming_shows=us,past_shows=ps)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id)
  form.name.data=artist.name
  form.city.data=artist.city
  form.state.data=artist.state
  form.phone.data=artist.phone
  form.genres.data=artist.genres
  form.facebook_link.data=artist.facebook_link
  form.website_link.data=artist.website_link
  form.image_link.data=artist.image_link
  form.seeking_description.data=artist.seeking_description
  form.seeking_venue.data=artist.seeking_venue
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error=""
  form=ArtistForm(request.form)
  artist=Artist.query.get(artist_id)
  if form.validate():
    try:
      artist.name=form.name.data
      artist.city=form.city.data
      artist.state=form.state.data
      artist.phone=form.phone.data
      artist.genres=form.genres.data
      artist.facebook_link=form.facebook_link.data
      artist.website_link=form.website_link.data
      artist.image_link=form.image_link.data
      artist.seeking_description=form.seeking_description.data
      artist.seeking_venue=form.seeking_venue.data
      db.session.add(artist)
      db.session.commit()
      flash('Artist' + request.form['name'] + ' was successfully edited')
    except:
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
    finally:
      db.session.close()
  else:
    #to get specific validation errors
    for name, errorMessages in form.errors.items():
      for err in errorMessages:
        print(name,err)
        error+=name+": "+err+"\n"
    flash('An error occurred.'+error)
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.get(venue_id)
  form.name.data=venue.name
  form.city.data=venue.city
  form.state.data=venue.state
  form.phone.data=venue.phone
  form.address.data=venue.address
  form.genres.data=venue.genres
  form.facebook_link.data=venue.facebook_link
  form.website_link.data=venue.website_link
  form.image_link.data=venue.image_link
  form.seeking_talent.data=venue.seeking_talent
  form.seeking_description.data=venue.seeking_description
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error=""
  form=VenueForm(request.form)
  venue=Venue.query.get(venue_id)
  if form.validate():
    try:
      venue.name=form.name.data
      venue.city=form.city.data
      venue.state=form.state.data
      venue.address=form.address.data
      venue.phone=form.phone.data
      venue.genres=form.genres.data
      venue.facebook_link=form.facebook_link.data
      venue.website_link=form.website_link.data
      venue.image_link=form.image_link.data
      venue.seeking_description=form.seeking_description.data
      venue.seeking_venue=form.seeking_talent.data
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully edited')
    except:
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')    
    finally:
      db.session.close()
  else:
    #to get specific validation errors
    for name, errorMessages in form.errors.items():
      for err in errorMessages:
        print(name,err)
        error+=name+": "+err+"\n"
    flash('An error occurred.'+error)
  return redirect(url_for('show_venue', venue_id=venue_id))
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error=""
  form=ArtistForm(request.form)
  if form.validate():
    try: 
      new_artist=Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        image_link=form.image_link.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data, 
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
      return redirect(url_for('index'))
  else:
    #to get specific validation errors
    for name, errorMessages in form.errors.items():
      for err in errorMessages:
        print(name,err)
        error+=name+": "+err+"\n"
    flash('An error occurred.'+error)
 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows=Show.query.all()
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form=ShowForm(request.form)
  if form.validate():
    try:
      new_show=Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data)
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
    except:
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
  else:
    flash('Something went wrong. Check your form.')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from flask import session as login_session
import random, string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Artist

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
    
APPLICATION_NAME = "Music Lovers"

# Connect to database and create database session
engine = create_engine('postgres://mcimbpchmgqyqq:HBafey8eKVFyTioeQFDSq4A3of@ec2-54-235-108-156.compute-1.amazonaws.com:5432/da1i6798elg6el')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    username = ''
    if 'username' in login_session:
        username = login_session['username']

    return render_template('login.html', STATE=state, username = username)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += "<h1>Welcome, %s </h1>" % login_session['username']
    flash("You are now logged in as %s" % login_session['username'])
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    if 'access_token' not in login_session:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        message = "You aren't logged in!"
    	return render_template('logout.html', message = message)

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
        message = 'Successfully disconnected!'
    	return render_template('logout.html', message = message)
    else:
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	message = 'An error occured!'
    	return render_template('logout.html', message = message)
        
@app.route('/')
@app.route('/genres')
def main():
    genres = session.query(Genre).all()
    username = ''
    if 'username' in login_session:
        username = login_session['username']
    return render_template('home.html', genres=genres, username=username)


""" Genre Views"""
@app.route('/genre/new', methods=['GET', 'POST'])
def add_genre():
    username = ''
    if 'username' in login_session:
        username = login_session['username']
    else:
        return redirect(url_for('show_login'))

    if request.method == 'GET':
        return render_template('add_genre.html', username=username)        
    if request.method == 'POST':
        name = request.form['name']
        if name:
            exists = session.query(Genre).filter_by(name=name).first()
            if exists:
                flash('That genre already exists!')
            else:
                newGenre = Genre(name = name)
                session.add(newGenre)
                session.commit()
                flash('Genre successfully added!')
        else:
            flash("Please enter a name")
            return redirect(url_for('add_genre'))
        return redirect(url_for('main'))
    
@app.route('/genre/<int:genre_id>')
def view_genre(genre_id):
    username = ''
    if 'username' in login_session:
        username = login_session['username']
    genre = session.query(Genre).get(genre_id)
    if genre:
        artists = session.query(Artist).filter_by(genre_id=genre.id)        
        return render_template('view_genre.html', genre=genre, artists=artists, username=username)
    else:
        abort(404)


@app.route('/genre/<int:genre_id>/edit', methods=['GET', 'POST'])
def edit_genre(genre_id):
    genre = session.query(Genre).get(genre_id)
    username = ''
    if 'username' in login_session:
        username = login_session['username']
    else:
        return redirect(url_for('show_login'))
    if genre:
        if request.method == 'GET':
            return render_template('edit_genre.html', genre=genre, username=username)
        if request.method == 'POST':
            name = request.form['name']
            if name:
                if name != genre.name:
                    exists = session.query(Genre).filter_by(name=name).first()
                    if exists:
                        flash("That genre already exists! Please rename it to something else")
                    else:
                        genre.name = name
                        session.add(genre)
                        session.commit()
                        flash('Genre info successfully edited!')
                        return redirect(url_for('view_genre', genre_id=genre_id))
                else:
                    flash('Please enter a different name than the original one')
            else:
                flash("Please enter a name")
            return redirect(url_for('edit_genre', genre_id=genre_id))
    else:
        abort(404)

@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
def delete_genre(genre_id):
    username = ''
    if 'username' in login_session:
        username = login_session['username']
    else:
        return redirect(url_for('show_login'))
    genre = session.query(Genre).get(genre_id)
    if genre:
        if request.method == 'POST':
            if genre:
                session.delete(genre)
                session.commit()
                flash("Genre successfully deleted!")
                return redirect(url_for('main'))
    else:
        abort(404)

""" Artist Views"""
@app.route('/genre/<int:genre_id>/artist/new', methods=['GET', 'POST'])
def add_artist(genre_id):
    username = ''
    if 'username' in login_session:
        username = login_session['username']
    else:
        return redirect(url_for('show_login'))
    genre = session.query(Genre).get(genre_id)
    if genre:
        if request.method == 'GET':
            return render_template('add_artist.html', genre = genre, username=username)
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            if name:
                exists = session.query(Artist).filter_by(name=name).first()
                if exists:
                    flash('That artist already exists!')
                else:
                    newArtist = Artist(name = name, description = description, genre_id = genre.id)
                    session.add(newArtist)
                    session.commit()
                    flash('Artist successfully added!')
            return redirect(url_for('view_genre', genre_id=genre_id))
    else:
        abort(404)

@app.route('/genre/<int:genre_id>/artist/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(genre_id, artist_id):
    username = ''
    if 'username' in login_session:
        username = login_session['username']
    else:
        return redirect(url_for('show_login'))
    genre = session.query(Genre).get(genre_id)
    artist = session.query(Artist).get(artist_id)
    if genre and artist:
        if request.method == 'GET':
            if artist:
                return render_template('edit_artist.html', genre=genre, artist=artist, username=username)
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            if name:
                if name != artist.name or description != artist.description:
                    exists = session.query(Artist).filter_by(name=name).first()
                    if exists and description == artist.description:
                        flash('That artist already exists! Please rename the artist to something else')
                    else:
                        artist.name = name
                        artist.description = description
                        session.add(artist)
                        session.commit()
                        flash('Artist info successfully edited!')
                        return redirect(url_for('view_genre', genre_id=genre_id))
                else:
                    flash('Please enter a different name than the original one')
            else:
                flash('Please enter a name')

            return redirect(url_for('edit_artist', genre_id=genre_id, artist_id=artist_id))
    else:
        abort(404)

@app.route('/genre/<int:genre_id>/artist/<int:artist_id>/delete', methods=['GET', 'POST'])
def delete_artist(genre_id, artist_id):
    username = ''
    if 'username' in login_session:
        username = login_session['username']
    else:
        return redirect(url_for('show_login'))
    artist = session.query(Artist).get(artist_id)
    if artist:
        if request.method == 'POST':
            if artist:
                session.delete(artist)
                session.commit()
                flash("Artist successfully deleted!")
                return redirect(url_for('view_genre', genre_id=genre_id))
    else:
        abort(404)

""" API Endpoints """
@app.route('/genre/JSON')
def view_genres_json():
    genres = session.query(Genre).all()
    if genres:
        return jsonify(Genres=[genre.serialize for genre in genres])
    else:
        abort(404)

@app.route('/genre/<int:genre_id>/JSON')
def view_genre_json(genre_id):
    genre = session.query(Genre).get(genre_id)
    if genre:
        return jsonify(Genre=genre.serialize)
    else:
        abort(404)

@app.route('/artist/JSON')
def view_artists_json():
    artists = session.query(Artist).all()
    if artists:
        return jsonify(Artists=[artist.serialize for artist in artists])
    else:
        abort(404)

@app.route('/genre/<int:genre_id>/artist/<int:artist_id>/JSON')
def view_artist_json(genre_id, artist_id):
    artist = session.query(Artist).get(artist_id)
    if artist:
        return jsonify(Artist=artist.serialize)
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
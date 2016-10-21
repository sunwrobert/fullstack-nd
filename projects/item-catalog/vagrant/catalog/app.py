from flask import Flask, render_template, request, redirect, url_for, flash, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Artist
app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True

engine = create_engine('postgres://mcimbpchmgqyqq:HBafey8eKVFyTioeQFDSq4A3of@ec2-54-235-108-156.compute-1.amazonaws.com:5432/da1i6798elg6el')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/genres')
def main():
    genres = session.query(Genre).all()
    return render_template('home.html', genres=genres)

""" Genre Views"""
@app.route('/genre/new', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'GET':
        return render_template('add_genre.html')        
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
    genre = session.query(Genre).get(genre_id)
    if genre:
        artists = session.query(Artist).filter_by(genre_id=genre.id)        
        return render_template('view_genre.html', genre=genre, artists=artists)
    else:
        abort(404)

@app.route('/genre/<int:genre_id>/edit', methods=['GET', 'POST'])
def edit_genre(genre_id):
    genre = session.query(Genre).get(genre_id)
    if genre:
        if request.method == 'GET':
            return render_template('edit_genre.html', genre=genre)
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
                        return redirect(url_for('main'))
                else:
                    flash('Please enter a different name than the original one')
            else:
                flash("Please enter a name")
            return redirect(url_for('edit_genre', genre_id=genre_id))
    else:
        abort(404)

@app.route('/genre/<int:genre_id>/delete', methods=['GET', 'POST'])
def delete_genre(genre_id):
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
    genre = session.query(Genre).get(genre_id)
    if genre:
        if request.method == 'GET':
            return render_template('add_artist.html', genre = genre)
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
    genre = session.query(Genre).get(genre_id)
    artist = session.query(Artist).get(artist_id)
    if genre and artist:
        if request.method == 'GET':
            if artist:
                return render_template('edit_artist.html', genre=genre, artist=artist)
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            if name:
                if name != artist.name:
                    exists = session.query(Artist).filter_by(name=name).first()
                    if exists:
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
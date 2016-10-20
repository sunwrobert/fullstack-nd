from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Artist
app = Flask(__name__)
app.secret = 'super_secret_key'
app.debug = True

engine = create_engine('postgres://mcimbpchmgqyqq:HBafey8eKVFyTioeQFDSq4A3of@ec2-54-235-108-156.compute-1.amazonaws.com:5432/da1i6798elg6el')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/genres')
def main():
    return 'main page'

@app.route('/genre/<int:genre_id>')
def view_genre(genre_id):
    return 'you are viewing %s' % genre_id

@app.route('/genre/<int:genre_id>/artist/<int:artist_id>')
def view_artist(genre_id, artist_id):
    return 'you are viewing %s in %s' % (artist_id, genre_id)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
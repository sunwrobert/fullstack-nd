from google.appengine.ext import db
from models.user import User
from models.post import Post


class Like(db.Model):
    post = db.ReferenceProperty(Post)
    user = db.ReferenceProperty(User)

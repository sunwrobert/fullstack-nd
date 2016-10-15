from google.appengine.ext import db
from jinja_helper import *
from models.post import Post
from models.user import User


class Comment(db.Model):
    post = db.ReferenceProperty(Post)
    content = db.TextProperty(required=True)
    author = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", comment=self)

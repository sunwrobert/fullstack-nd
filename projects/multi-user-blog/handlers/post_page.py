from blog_handler import BlogHandler
from models.post import Post
from models.like import Like
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        like = Like.all().filter('post =', post.key()).filter('user =', self.user)
        num_likes = like.count()
        error = self.request.get("error")
        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post, error = error, num_likes = num_likes)
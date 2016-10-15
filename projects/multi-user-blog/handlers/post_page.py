from blog_handler import BlogHandler
from models.post import Post
from models.like import Like
from models.comment import Comment
from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class PostPage(BlogHandler):

    """ Handler for the permalink post page

    GET: Get all the posts, the number of likes associated with that post,
    and the comments associated with that post and then render it to the
    screen. Can also render optional error and regular messages

    """

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        like = Like.all().filter(
            'post =', post.key()).filter('user =', self.user)
        num_likes = like.count()
        comments = Comment.all().filter('post =', post.key())
        error = self.request.get("error")
        message = self.request.get("message")
        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post, error=error,
                    num_likes=num_likes, comments=comments, message=message)

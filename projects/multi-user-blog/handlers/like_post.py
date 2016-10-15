from blog_handler import BlogHandler
from models.post import Post
from models.like import Like
from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class LikePost(BlogHandler):

    """ Handler for liking posts

    No GET request because there is no page for them to visit
    POST: Adds a Like to the database if there is no like yet. If there is,
    redirect to the post page with a message saying they've already liked
    the post.

    """

    def post(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if post.author.name != self.user.name:
                like = Like.all().filter('post =', post.key()).filter(
                    'user =', self.user.key()).get()
                if not like:
                    l = Like(post=post, user=self.user)
                    l.put()
                    self.redirect(
                        "/blog/%s?message=You liked the post!" % post_id)
                else:
                    self.redirect(
                        "/blog/%s?message=You already liked this post!"
                        % post_id)
            else:
                self.redirect(
                    "/blog/%s?error=You can't like your own post!" % post_id)
        else:
            self.redirect(
                "/login?error=You need to be logged, in order to like a post")

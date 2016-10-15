from blog_handler import BlogHandler
from models.post import Post
from google.appengine.ext import db
from models.comment import Comment


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class CommentPage(BlogHandler):

    """ Handler for the add comment page

    GET: Renders the add comment form and takes in the post_id for a back link.
    POST: Adds a new comment if the form validation passes.

    """

    def get(self, post_id):
        if self.user:
            self.render("addcomment.html", post_id=post_id)
        else:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            return self.redirect('/blog')

        content = self.request.get('content')

        if content:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            c = Comment(parent=blog_key(), post=post, content=content,
                        author=self.user)
            c.put()
            self.redirect('/blog/%s?message=Comment successfully added!'
                          % str(post.key().id()))
        else:
            error = "Please enter some content"
            self.render("addcomment.html", post_id=post_id, content=content,
                        error=error)

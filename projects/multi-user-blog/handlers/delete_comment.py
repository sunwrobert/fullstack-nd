from blog_handler import BlogHandler
from models.comment import Comment
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class DeleteComment(BlogHandler):
    """ Handler for deleting comments

    There is no GET because users shouldn't be visiting this
    POST: Get the comment based on comment id and check if the current user is the
    same as the comment's user. If so, delete the comment. Else, redirect with an error

    """
    def post(self, post_id, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id), parent=blog_key())
            comment = db.get(key)
            if comment.author.name == self.user.name:
                comment.delete()
                self.redirect("/blog/%s?message=Deleted comment successfully!" % post_id)
            else:
                self.redirect("/blog/%s?error=You don't have access to delete this comment." % post_id)
        else:
            self.redirect("/login?error=You need to be logged, in order to delete a post")
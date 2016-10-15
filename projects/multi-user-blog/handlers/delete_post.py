from blog_handler import BlogHandler
from models.post import Post
from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class DeletePost(BlogHandler):

    """ Handler for deleting posts

    There is no GET because users shouldn't be visiting this
    POST: Get the post based on post id and check if the current user is the
    same as the comment's user. If so, delete the post. Else,
    redirect with an error

    """

    def post(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if post.author.name == self.user.name:
                post.delete()
                self.redirect("/blog?message=Deleted post successfully!")
            else:
                self.redirect(
                    "/blog/%s?error=You don't have access to delete this post."
                    % post_id)
        else:
            self.redirect(
                "/login?error=You need to be logged, in order to delete " +
                "a post")

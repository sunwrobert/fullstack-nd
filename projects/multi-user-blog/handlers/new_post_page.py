from blog_handler import BlogHandler
from models.post import Post
from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class NewPost(BlogHandler):

    """ Handler for making a new post

    GET: Render the new post page
    POST: Do form validation and then check if the author has permission.
    If so, make a new post. Else, redirect to the blog with an error

    """

    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            return self.redirect("/login")

    def post(self):
        if not self.user:
            return self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent=blog_key(), subject=subject,
                     content=content, author=self.user)
            p.put()
            return self.redirect(
                '/blog/%s?message=Post successfully created!'
                % str(p.key().id()))
        else:
            error = "Please enter the subject and content."
            self.render(
                "newpost.html", subject=subject, content=content, error=error)

from blog_handler import BlogHandler
from models.post import Post
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, author=self.user)
            p.put()
            self.redirect('/blog/%s?message=Post successfully created!' % str(p.key().id()))
        else:
            error = "Please enter the subject and content."
            self.render("newpost.html", subject=subject, content=content, error=error)
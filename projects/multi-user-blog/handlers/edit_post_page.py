from blog_handler import BlogHandler
from models.post import Post
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class EditPost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            error = ''
            if not post:
                self.error(404)
                return
            
            if post.author.name != self.user.name:
                self.redirect('/blog/%s' % post_id)
            
            self.render("editpost.html", subject=post.subject, content=post.content, error=error)
        else:
            self.redirect("/login")
    
    def post(self, post_id):
        if self.user:
            subject = self.request.get('subject')
            content = self.request.get('content')

            if subject and content:
                key = db.Key.from_path('Post', int(post_id), parent=blog_key())
                post = db.get(key)
                if post.author.name == self.user.name:
                    post.subject = subject
                    post.content = content
                    post.put()
                    self.redirect('/blog/%s' % post_id)
                else:
                    self.redirect('/blog/%s' % post_id)
            else:
                error = "Please enter the subject and content."
                self.render("editpost.html", subject=subject, content=content, error=error)
        else:
            self.redirect('/login')

        
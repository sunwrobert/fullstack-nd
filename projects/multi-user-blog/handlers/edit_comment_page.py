from blog_handler import BlogHandler
from models.post import Post
from models.comment import Comment
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class EditComment(BlogHandler):
    def get(self, post_id, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id), parent=blog_key())
            comment = db.get(key)
            if not comment:
                self.error(404)
                return
            
            if comment.author.name != self.user.name:
                self.redirect("/blog/%s?error=You don't have access to edit this comment." % post_id)
            
            self.render("editcomment.html", content=comment.content)
        else:
            self.redirect("/login")
    
    def post(self, post_id, comment_id):
        if self.user:
            content = self.request.get('content')

            if content:
                key = db.Key.from_path('Comment', int(comment_id), parent=blog_key())
                comment = db.get(key)
                if comment.author.name == self.user.name:
                    comment.content = content
                    comment.put()
                    self.redirect("/blog/%s?message=Comment successfully edited!" % post_id)
                else:
                    self.redirect("/blog/%s?error=You don't have access to edit this comment." % post_id)
            else:
                error = "Please enter some content."
                self.render("editcomment.html", content=content, error=error)
        else:
            self.redirect('/login')

        
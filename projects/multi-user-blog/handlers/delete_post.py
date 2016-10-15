from blog_handler import BlogHandler
from models.post import Post
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
    
class DeletePost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if post.author.name == self.user.name:
                post.delete()
                self.redirect("/blog?delete=Deleted post successfully!")
            else:
                self.redirect("/blog/" + post_id + "?error=You don't have access to delete this post.")
        else:
            self.redirect("/login?error=You need to be logged, in order to delete your post")
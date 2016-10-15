from blog_handler import BlogHandler
from models.post import Post

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
    
class BlogFront(BlogHandler):
    def get(self):
        posts = Post.all().order('-created')
        message = self.request.get("message")
        self.render('front.html', posts = posts, message = message)
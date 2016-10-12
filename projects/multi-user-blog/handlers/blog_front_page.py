from blog_handler import BlogHandler
from models.post import Post

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
    
class BlogFront(BlogHandler):
    def get(self):
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts = posts)
from blog_handler import BlogHandler
from models.post import Post

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
    
class BlogFront(BlogHandler):
    """ Handler for blog front

    GET: Renders the last 10 posts and optional messages sent from other pages

    """
    def get(self):
        posts = Post.all().order('-created').run(limit = 10)
        message = self.request.get("message")
        self.render('front.html', posts = posts, message = message)
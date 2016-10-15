from blog_handler import BlogHandler


class MainPage(BlogHandler):

    def get(self):
        self.redirect('/blog')

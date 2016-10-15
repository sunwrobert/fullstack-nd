from handlers.blog_handler import BlogHandler

class Logout(BlogHandler):
    def get(self):
        if self.user:
            self.logout()
            self.render("logout.html")
        else:
            self.redirect('/blog')
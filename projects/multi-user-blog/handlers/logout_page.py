from handlers.blog_handler import BlogHandler


class Logout(BlogHandler):

    """ Handler for logout page

    GET: Logout and render the logout page

    """

    def get(self):
        if self.user:
            self.logout()
            self.render("logout.html")
        else:
            self.redirect('/blog')

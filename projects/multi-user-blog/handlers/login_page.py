from handlers.blog_handler import BlogHandler
from models.user import User

class Login(BlogHandler):
    """ Handler for login page

    GET: Simply render the login form html page
    POST: Form validation with proper redirects based on if the form is valid and the user exists or not.

    """
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog?message=Successfully logged in!')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)
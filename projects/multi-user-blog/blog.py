import re
from google.appengine.ext import db
from jinja_helper import *
import webapp2

from models.user import User
from models.post import Post

from handlers.blog_handler import BlogHandler

from handlers.main_page import MainPage
from handlers.blog_front_page import BlogFront
from handlers.post_page import PostPage
from handlers.new_post_page import NewPost
from handlers.edit_post_page import EditPost
from handlers.delete_post import DeletePost
from handlers.like_post import LikePost
from handlers.signup_page import Signup
from handlers.login_page import Login
from handlers.logout_page import Logout

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/([0-9]+)/edit', EditPost),
                               ('/blog/([0-9]+)/delete', DeletePost),
                               ('/blog/([0-9]+)/like', LikePost),
                               ('/blog/newpost', NewPost),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ],
                              debug=True)
